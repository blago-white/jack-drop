import hashlib

from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.request import Request

from common.repositories.products import ProductsApiRepository
from common.repositories.users import UsersRepository
from common.views.api import BaseCreateApiView, BaseApiView
from ..repositories.transactions import PaymentsRepository
from ..serializers import TransactionCreationPubllicSerializer


class NicepayInitReplenishApiView(BaseCreateApiView):
    payments_repository = PaymentsRepository()
    users_repository = UsersRepository()
    products_repository = ProductsApiRepository()

    serializer_class = TransactionCreationPubllicSerializer

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get_info(user_request=request)

        deposit_data = self._complete_dataset(
            user_data=user_data
        )

        free_deposit_case = self.products_repository.get_free_case_for_deposit(
            deposit_amount=deposit_data.get("amount")
        )

        payment = self.payments_repository.nicepay_create(
            data=deposit_data,
            free_deposit_case=free_deposit_case
        )

        return self.get_201_response(
            data=payment
        )

    def _complete_dataset(self, user_data: dict):
        return dict(
            user_login=user_data.get("username"),
            user_id=user_data.get("id"),
            amount=self.request.data.get("amount"),
            promocode=self.request.data.get("promocode")
        )


class SkinifyInitReplenishApiView(BaseCreateApiView):
    payments_repository = PaymentsRepository()
    users_repository = UsersRepository()

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get_info(user_request=request)

        print(request.data, user_data)

        payment = self.payments_repository.skinify_create(
            data=request.data | user_data
        )

        return self.get_201_response(
            data=payment
        )


class NicePayTransactionCallbackApiView(BaseApiView, ListAPIView):
    payments_repository = PaymentsRepository()
    users_repository = UsersRepository()
    products_repository = ProductsApiRepository()

    def get(self, request: Request, *args, **kwargs):
        tid = request.query_params.get("order_id")

        self._authenticate(dict(request.query_params).copy())

        tstatus = request.query_params.get("result")

        self.payments_repository.nicepay_update(
            tid=tid,
            data=request.query_params
        )

        if tstatus == "success":
            used_promocode = self.payments_repository.get_promocode(tid=tid)

            deposit = self.users_repository.add_depo(
                amount=float(request.query_params.get("amount")) / 100,
                currency=request.query_params.get("amount_currency"),
                user_id=self.payments_repository.get_payeer_id(tid=tid),
                promocode=used_promocode
            )

            self.products_repository.send_deposit_callback(data={
                "user_id": deposit.get("user_id"),
                "deposit_id": deposit.get("id"),
                "amount": deposit.get("amount")
            })

        return self.get_200_response()

    def _authenticate(self, data: dict[str, str]):
        validate_hash = data.pop("hash")

        sorted_params = sorted([(i[0], i[-1][0]) for i in data.copy().items()])

        sorted_params.append(
            ("secret_key", self.payments_repository.nicepay_secret_for_validation)
        )

        params = "{np}".join([str(i[-1]) for i in sorted_params])

        params_hash = hashlib.sha256(params.encode()).hexdigest()

        if params_hash != validate_hash[0]:
            raise ValidationError("Error validate signature")


class SkinifyTransactionCallbackApiView(BaseCreateApiView):
    payments_repository = PaymentsRepository()
    users_repository = UsersRepository()
    products_repository = ProductsApiRepository()

    def create(self, request: Request, *args, **kwargs):
        request_data = dict(request.data)

        if type(request_data.get("deposit_id")) == list:
            request_data = {
                key: (int(request_data[key][0]) if request_data[key][0].isdigit() else request_data[key][0])
                for key in request_data
            }

        print(request_data)

        tid = request_data.get("deposit_id")

        self._authenticate(dict(request_data).copy())

        tstatus = request_data.get("status")

        print(tstatus)

        self.payments_repository.skinify_update(
            tid=tid, data=request_data
        )

        if tstatus == "success":
            used_promocode = self.payments_repository.get_promocode(tid=tid)

            deposit = self.users_repository.add_depo(
                amount=float(request_data.get("amount")),
                currency=request_data.get("amount_currency"),
                user_id=self.payments_repository.get_payeer_id(tid=tid),
                promocode=used_promocode
            )

            self.products_repository.send_deposit_callback(data={
                "user_id": deposit.get("user_id"),
                "deposit_id": deposit.get("id"),
                "amount": deposit.get("amount")
            })

        return self.get_200_response()

    def _authenticate(self, data: dict[str, str]):
        validate_hash = data.pop("token_md5")

        if validate_hash != hashlib.md5(
            self.payments_repository.skinify_secret_for_validation.encode()
        ).hexdigest():
            print("ERRROR VALIDATE SIGN", validate_hash, self.payments_repository.skinify_secret_for_validation, hashlib.md5(
            self.payments_repository.skinify_secret_for_validation.encode()
        ).hexdigest())

            raise ValidationError("Error validate signature")


class TransactionValidationApiView(BaseApiView, RetrieveAPIView):
    repository = PaymentsRepository()
    serializer_class = None

    def retrieve(self, request, *args, **kwargs):
        if self.repository.transaction_exists(
            tid=request.data.get("transaction_id"),
            user_id=request.data.get("user_id")
        ):
            return self.get_200_response()

        raise ValidationError(code=400, detail="Transaction does not exists!")
