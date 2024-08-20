from rest_framework.generics import CreateAPIView

from common.views.api import BaseCreateApiView
from common.repositories.users import UsersRepository

from ..repositories.transactions import CardPaymentsRepository
from ..serializers import TransactionCreationPubllicSerializer


class InitReplenishApiView(BaseCreateApiView):
    payments_repository = CardPaymentsRepository()
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

