from cases.repositories.case import CasesRepository
from common.mixins.api import CreateAPIViewMixin
from games.repositories.api.drop import CaseDropApiRepository
from games.repositories.api.users import UsersApiRepository
from games.serializers.drop import DropItemGameApiViewSerializer

from .base import BaseGameProxyCreateApiView


class DropItemGameApiView(CreateAPIViewMixin, BaseGameProxyCreateApiView):
    users_api_repository = UsersApiRepository()
    cases_repository = CasesRepository()
    drop_api_repository = CaseDropApiRepository()

    serializer_class = DropItemGameApiViewSerializer

    pk_url_kwarg = "case_id"

    def create(self, request, *args, **kwargs):
        user_funds = self.users_api_repository.get(
            user_request=request
        )

        case_data = self.cases_repository.get(
            case_id=self.get_requested_pk()
        )

        result = self.drop_api_repository.drop(
            data=user_funds | case_data
        )

        self.users_api_repository.update_balance(
            user_request=request,
            delta_amount=(-case_data.get("price"))
        )

        return self.get_201_response(data=result)
