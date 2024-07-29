from rest_framework.request import Request

from battles.repositories.battle import BattleRequestRepository
from common.views.api import DefaultCreateApiView, DefaultDeleteApiView, DefaultRetrieveApiView


class StartBattleRequestApiView(DefaultCreateApiView):
    repository = BattleRequestRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        print("MAKE REQUEST")

        return self.get_201_response(
            data=self.repository.create(request_data=request.data)
        )


class DropBattleRequestApiView(DefaultDeleteApiView):
    repository = BattleRequestRepository()
    serializer_class = repository.default_serializer_class
    pk_url_kwarg = "initiator_id"

    def destroy(self, request, *args, **kwargs):
        print("DROP REQUEST")

        return self.get_200_response(
            data=self.repository.drop(initiator_id=self.get_requested_pk())
        )


class CurrentBattleRequestsApiView(DefaultRetrieveApiView):
    repository = BattleRequestRepository()
    serializer_class = repository.default_serializer_class
    pk_url_kwarg = "case_id"

    def retrieve(self, request: Request, *args, **kwargs):
        result = self.repository.all(case_id=self.get_requested_pk())

        return self.get_200_response(
            data=result
        )


class CurrentBattleRequestsCountApiView(DefaultRetrieveApiView):
    repository = BattleRequestRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request: Request, *args, **kwargs):
        result = self.repository.count_by_case()

        return self.get_200_response(
            data=result
        )
