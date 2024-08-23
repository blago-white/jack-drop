from rest_framework.generics import CreateAPIView

from common.mixins.api import CreateAPIViewMixin

from bonus.repositories.free import FreeCasesRepository


class DepositWebHookApiView(CreateAPIViewMixin, CreateAPIView):
    _repository = FreeCasesRepository()
    serializer_class = _repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        print("DEPOSIT WEBHOOK", request.data)

        return self.get_201_response(
            data=self._repository.add(request_data=request.data)
        )
