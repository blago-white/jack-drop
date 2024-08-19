from rest_framework.generics import CreateAPIView

from common.views.api import BaseCreateApiView
from ..repositories.transactions import CardPaymentsRepository


class CreateTransactionApiView(BaseCreateApiView):
    repository = CardPaymentsRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            data=self.repository.create(request_data=request.data)
        )
