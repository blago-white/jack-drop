from cases.repositories.case import CasesRepository
from common.mixins.api import CreateAPIViewMixin, DetailedApiViewMixin
from games.repositories.api.drop import CaseDropApiRepository, DropItemsRepository
from games.repositories.api.users import UsersApiRepository
from games.serializers.drop import DropItemGameApiViewSerializer

from .base import BaseGameProxyCreateApiView


class DropItemGameApiView(DetailedApiViewMixin,
                          CreateAPIViewMixin,
                          BaseGameProxyCreateApiView):
    users_api_repository = UsersApiRepository()
    cases_repository = CasesRepository()
    case_items_repository = DropItemsRepository()
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

        case_items = self.case_items_repository.get_drop_items_by_case(
            case_pk=case_data.get("id")
        )

        result = self.drop_api_repository.drop(
            user_funds=user_funds,
            case_data=case_data | {"items": case_items}
        )

        return self.get_201_response(data=result)
