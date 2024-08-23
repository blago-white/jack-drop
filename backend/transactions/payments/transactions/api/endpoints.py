from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError

from common.views.api import BaseCreateApiView, BaseApiView
from common.repositories.users import UsersRepository

from ..repositories.transactions import PaymentsRepository
from ..serializers import TransactionCreationPubllicSerializer


class InitReplenishApiView(BaseCreateApiView):
    payments_repository = PaymentsRepository()
    users_repository = UsersRepository()

    serializer_class = TransactionCreationPubllicSerializer

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get_info(user_request=request)

        payment = self.payments_repository.create(data=self._complete_dataset(
            user_data=user_data
        ))

        return self.get_201_response(
            data=payment
        )

    def _complete_dataset(self, user_data: dict):
        return dict(
            user_id=user_data.get("id"),
            username=user_data.get("username"),
            user_ip=self._get_ip(),
            pay_method=self.request.data.get("pay_method"),
            amount=self.request.data.get("amount"),
        )

    def _get_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        else:
            return self.request.META.get('REMOTE_ADDR')


class TransactionCallbackApiView(BaseApiView, RetrieveAPIView):
    payments_repository = PaymentsRepository()
    users_repository = UsersRepository()

    def retrieve(self, request: Request, *args, **kwargs):
        result = self.payments_repository.close(callback_data=request.data)

        if not result.get("aborted"):
            self.users_repository.add_depo(
                amount=result.get("amount"),
                user_id=self.payments_repository.get_payeer_id(
                    tid=request.data.get("tid"),
                    amount=result.get("amount")
                )
            )

        return result


class TransactionValidationApiView(BaseApiView, RetrieveAPIView):
    repository = PaymentsRepository()
    serializer_class = None

    def retrieve(self, request, *args, **kwargs):
        if self.repository.transaction_exists(
            tid=request.data.get("transaction_id"),
            amount=request.data.get("amount"),
            user_id=request.data.get("user_id")
        ):
            return self.get_200_response()

        raise ValidationError(code=400, detail="Transaction does not exists!")
