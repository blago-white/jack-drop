from rest_framework.request import Request
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from games.repositories.api.users import UsersApiRepository
from common.views.api import BaseListAPIView, DetailedApiViewMixin
from common.mixins.api import CreateAPIViewMixin
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


class ItemSetDetailedApiView(DetailedApiViewMixin, RetrieveAPIView):
    repository = ItemsSetsRepository()
    pk_url_kwarg = "set_id"

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get(
                set_id=self.get_requested_pk()
            )
        )


class ItemSetBuyApiView(DetailedApiViewMixin, CreateAPIViewMixin, CreateAPIView):
    repository = ItemsSetsRepository()
    users_repository = UsersApiRepository()
    pk_url_kwarg = "set_id"

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get(
            user_request=request
        )

        return self.get_201_response(
            data=self.repository.buy(
                user_data=user_data,
                set_id=self.get_requested_pk()
            )
        )
