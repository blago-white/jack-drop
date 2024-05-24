from common.views.api import DefaultCreateApiView, DefaultDeleteApiView

from battles.repositories.battle import BattleRequestRepository


class CommitBattleApiView(DefaultCreateApiView):
    repository = BattleRequestRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            data=self.repository.create(request_data=request)
        )
