import hashlib

from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.request import Request

from common.repositories.products import ProductsApiRepository
from common.repositories.users import UsersRepository
from common.views.api import BaseCreateApiView, BaseApiView
from ..repositories.transactions import PaymentsRepository
from ..serializers import TransactionCreationPubllicSerializer


class InitReplenishApiView(BaseCreateApiView):
    payments_repository = PaymentsRepository()
    users_repository = UsersRepository()

    serializer_class = TransactionCreationPubllicSerializer

    def create(self, request, *args, **kwargs):
        print("START")

        user_data = self.users_repository.get_info(user_request=request)

        payment = self.payments_repository.create(data=self._complete_dataset(
            user_data=user_data
        ))

        print("INITED PAYMENT", payment)

        return self.get_201_response(
            data=payment
        )

    def _complete_dataset(self, user_data: dict):
        return dict(
            user_login=user_data.get("username"),
            user_id=user_data.get("id"),
            amount=self.request.data.get("amount"),
        )


class TransactionCallbackApiView(BaseApiView, ListAPIView):
    payments_repository = PaymentsRepository()
    users_repository = UsersRepository()
    products_repository = ProductsApiRepository()

    def get(self, request: Request, *args, **kwargs):
        print("HANDLE CALLBACK", request.query_params)

        tid = request.query_params.get("order_id")

        self._authenticate(dict(request.query_params).copy())

        print(f"CALLBACK REQUEST: {dict(request.query_params)}")

        tstatus = request.query_params.get("result")

        self.payments_repository.update(
            tid=tid,
            data=request.query_params
        )

        if tstatus == "success":
            deposit = self.users_repository.add_depo(
                amount=float(request.query_params.get("amount")) / 100,
                currency=request.query_params.get("amount_currency"),
                user_id=self.payments_repository.get_payeer_id(tid=tid)
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
            ("secret_key", self.payments_repository.secret_for_validation)
        )

        params = "{np}".join([str(i[-1]) for i in sorted_params])

        params_hash = hashlib.sha256(params.encode()).hexdigest()

        if params_hash != validate_hash[0]:
            print("PAYMENT SIGN VALIDATION ERROR")
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
