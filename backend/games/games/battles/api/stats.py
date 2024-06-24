from rest_framework.generics import ListAPIView

from common.views.api import DefaultRetrieveApiView
from common.mixins.api.base import ApiViewMixin

from ..repositories.battle import BattleRepository


class BattlesStatsApiView(DefaultRetrieveApiView):
    repository = BattleRepository()
    pk_url_kwarg = "user_id"

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get_stats(user_id=self.get_requested_pk())
        )


class BattlesHistoryApiView(DefaultRetrieveApiView):
    repository = BattleRepository()
    pk_url_kwarg = "user_id"

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get_history(user_id=self.get_requested_pk())
        )
