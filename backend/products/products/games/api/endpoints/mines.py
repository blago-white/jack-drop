from rest_framework.generics import UpdateAPIView, DestroyAPIView

from common.mixins.api import CreateAPIViewMixin
from games.repositories.api.mines import MinesGameApiRepository
from games.repositories.api.users import UsersApiRepository
from games.serializers.mines import MinesGameRequestViewSerializer
from .base import BaseGameProxyCreateApiView


class MinesGameApiView(CreateAPIViewMixin, BaseGameProxyCreateApiView):
    _repository = MinesGameApiRepository()
    users_api_repository = UsersApiRepository()
    serializer_class = MinesGameRequestViewSerializer

    def create(self, request, *args, **kwargs):
        print("START")

        user_data = self.users_api_repository.get(
            user_request=request
        )

        print("FUNDS")

        result = self._repository.init(
            request_data=request.data,
            user_data=user_data
        )

        print("INITED")

        return self.get_201_response(
            data=result
        )


class MinesGameNextStepApiView(CreateAPIViewMixin, UpdateAPIView):
    _repository = MinesGameApiRepository()
    users_api_repository = UsersApiRepository()

    def update(self, request, *args, **kwargs):
        user_data = self.users_api_repository.get(
            user_request=request
        )

        result = self._repository.next(
            user_id=user_data.get("id")
        )

        return self.get_201_response(
            data=result
        )


class MinesGameStopApiView(CreateAPIViewMixin, DestroyAPIView):
    _repository = MinesGameApiRepository()
    users_api_repository = UsersApiRepository()

    def destroy(self, request, *args, **kwargs):
        user_data = self.users_api_repository.get(
            user_request=request
        )

        result = self._repository.stop(
            user_id=user_data.get("id")
        )

        return self.get_201_response(
            data=result
        )
