from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError

from common.views.api import BaseCreateApiView, BaseApiView
from common.repositories.users import UsersRepository
from common.repositories.products import ProductsApiRepository

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
            user_id=user_data.get("id"),
            amount=self.request.data.get("amount"),
        )


class TransactionCallbackApiView(BaseCreateApiView):
    payments_repository = PaymentsRepository()
    users_repository = UsersRepository()
    products_repository = ProductsApiRepository()

    def create(self, request: Request, *args, **kwargs):
        print("START VIEW")

        tid = request.data.get("transaction").get("invoice_id")

        self._authenticate(tid)

        tstatus = request.data.get("status")

        self.payments_repository.update(
            tid=tid,
            data=request.data
        )

        if tstatus == "CONFIRMED":
            deposit = self.users_repository.add_depo(
                amount=request.get("transaction").get("pricing").get(
                    "local"
                ).get("amount"),
                currency=request.get("transaction").get("pricing").get(
                    "local"
                ).get("currency"),
                user_id=self.payments_repository.get_payeer_id(tid=tid)
            )

            self.products_repository.send_deposit_callback(data={
                "user_id": deposit.get("user_id"),
                "deposit_id": deposit.get("id"),
                "amount": deposit.get("amount")
            })

        return self.get_200_response()

    def _authenticate(self, tid: int):
        ...


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
