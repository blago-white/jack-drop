from common.views.base import BaseCreateApiView, BaseRetrieveApiView

from ..repositories.dinamic import DinamicFundsRepository


class IncreaseDinamicFundsApiView(BaseCreateApiView):
    repository = DinamicFundsRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        return self._get_201_response(
            data=self.repository.increase(data=request.data)
        )


class DecreaseDinamicFundsApiView(BaseCreateApiView):
    repository = DinamicFundsRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        return self._get_201_response(
            data=self.repository.decrease(data=request.data)
        )


class RetrieveDinamicFundsApiView(BaseRetrieveApiView):
    repository = DinamicFundsRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request, *args, **kwargs):
        return self._get_200_response(
            data=self.repository.get()
        )
