from common.views.api import DefaultCreateApiView

from battles.repositories.battle import BattleRepository
from common.views.api import DefaultCreateApiView


class MakeBattleApiView(DefaultCreateApiView):
    repository = BattleRepository()
    serializer_class = repository.default_serializer_class
    pk_url_kwarg = "initiator_id"

    def create(self, request, *args, **kwargs):
        result = self.repository.make(
            request_data=request.data
        )

        return self.get_200_response(
            data=result
        )
