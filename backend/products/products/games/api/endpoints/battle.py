from .base import BaseGameProxyCreateApiView

from common.mixins.api import CreateApiViewMixin
from games.repositories.api.battle import BattleRequestApiRepository
from games.repositories.api.users import UsersApiRepository
from games.serializers.battle import BattleRequestApiViewSerializer


class CreateBattleRequestApiView(CreateApiViewMixin,
                                 BaseGameProxyCreateApiView):
    battle_repository = BattleRequestApiRepository()
    users_repository = UsersApiRepository()

    serializer_class = BattleRequestApiViewSerializer

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get(user_request=request)

        created = self.battle_repository.create(
            battle_case_id=request.data.get("battle_case_id"),
            user_data=user_data
        )

        return self.get_201_response(
            data=created
        )


class DropBattleRequestApiView(CreateApiViewMixin,
                               BaseGameProxyCreateApiView):
    battle_repository = BattleRequestApiRepository()
    users_repository = UsersApiRepository()

    serializer_class = BattleRequestApiViewSerializer

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get(user_request=request)

        created = self.battle_repository.create(
            battle_case_id=request.data.get("battle_case_id"),
            user_data=user_data
        )

        return self.get_201_response(
            data=created
        )
