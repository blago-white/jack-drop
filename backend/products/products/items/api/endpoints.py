from rest_framework.request import Request

from common.views.api import BaseListAPIView
from ..repositories.items import ItemsRepository
from ..repositories.sets import ItemsSetsRepository


class ItemsListApiView(BaseListAPIView):
    _repository = ItemsRepository()
    serializer_class = _repository.default_serializer_class

    def list(self, request: Request, *args, **kwargs):
        return self.get_200_response(
            data=self._repository.get_all(
                min_price=request.query_params.get("min"),
                max_price=request.query_params.get("max")
            )
        )


class ItemsSetsListApiView(BaseListAPIView):
    _repository = ItemsSetsRepository()

    def list(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self._repository.get_all()
        )
