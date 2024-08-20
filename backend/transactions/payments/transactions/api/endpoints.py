from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request

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
        return self.repository.default_serializer_class(
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
                    tid=request.get("tid"),
                    amount=result.get("amount")
                )
            )

        return result
