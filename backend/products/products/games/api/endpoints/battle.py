from common.views.api import BaseListAPIView

from games.repositories.api.users import UsersApiRepository
from games.repositories.api.battle import BattleApiRepository


class BattleStatsApiView(BaseListAPIView):
    _users_repository = UsersApiRepository()
    _battle_repository = BattleApiRepository()

    def list(self, request, *args, **kwargs):
        user_data = self._users_repository.get(user_request=request)

        return self.get_200_response(
            data=self._battle_repository.get_stats(user_id=user_data.get("id"))
        )


class BattlesHistoryApiView(BaseListAPIView):
    _users_repository = UsersApiRepository()
    _battle_repository = BattleApiRepository()

    def list(self, request, *args, **kwargs):
        user_data = self._users_repository.get(user_request=request)

        return self.get_200_response(
            data=self._battle_repository.get_all(user_id=user_data.get("id"))
        )
