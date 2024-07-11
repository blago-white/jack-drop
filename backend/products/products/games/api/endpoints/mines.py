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
        user_data = self.users_api_repository.get(
            user_request=request
        )

        result = self._repository.make(
            request_data=request.data,
            user_data=user_data
        )

        user_balance_diff = result.get("funds_difference").get("user_funds_diff")
        mines_game = result.get("mines_game")

        return self.get_201_response(
            data={"user_funds_diff": user_balance_diff} | mines_game
        )
