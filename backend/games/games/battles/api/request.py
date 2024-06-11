from common.views.api import DefaultCreateApiView, DefaultDeleteApiView

from battles.repositories.battle import BattleRequestRepository, BattleRepository


class StartBattleRequestApiView(DefaultCreateApiView):
    repository = BattleRequestRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            data=self.repository.create(request_data=request)
        )


class DropBattleRequestApiView(DefaultDeleteApiView):
    repository = BattleRequestRepository()
    serializer_class = repository.default_serializer_class
    pk_url_kwarg = "initiator_id"

    def destroy(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.drop(initiator_id=self.get_requested_pk())
        )


class MakeBattleApiView(DefaultDeleteApiView):
    repository = BattleRepository()
    serializer_class = repository.default_serializer_class
    pk_url_kwarg = "initiator_id"

    def create(self, request, *args, **kwargs):
        initiator = request

        return self.get_200_response(
            data=self.repository.make(

            )
        )
