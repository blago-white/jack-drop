from rest_framework.generics import CreateAPIView

from ..repositories.transactions import CardPaymentsRepository


class CreateTransactionApiView(CreateAPIView):
    repository = CardPaymentsRepository()

    def create(self, request, *args, **kwargs):
        pass
