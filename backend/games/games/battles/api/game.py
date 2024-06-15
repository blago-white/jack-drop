import json

from common.views.api import DefaultCreateApiView

from battles.repositories.battle import BattleRequestRepository, BattleRepository


class MakeBattleApiView(DefaultCreateApiView):
    repository = BattleRepository()
    serializer_class = repository.default_serializer_class
    pk_url_kwarg = "initiator_id"

    def create(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.make(
                request_data=request.data
            )
        )
