from django.http.request import HttpRequest

from common.repositories import BaseRepository
from common.states import FoundsState

from common.services.api.cases import CasesApiService
from common.services.api.users import UsersApiService
from ..services.drop import CaseItemDropModelService
from ..states.request import DropRequest
from ..serializers import DroppedCaseItemSerializer


class CaseItemDropRepository(BaseRepository):
    default_service = CaseItemDropModelService()
    default_serializer_class = DroppedCaseItemSerializer
    _service: CaseItemDropModelService
    _products_web_service: CasesApiService
    _users_web_service: UsersApiService

    def __init__(self, *args,
                 products_web_service: CasesApiService = CasesApiService(),
                 users_web_service: UsersApiService = UsersApiService(),
                 **kwargs):
        self._products_web_service = products_web_service
        self._users_web_service = users_web_service

        super().__init__(*args, **kwargs)

    def get(self, request: HttpRequest, case_id: int) -> dict:
        case_data = self._products_web_service.get_info(
            case_id=case_id
        )

        advantage = self._users_web_service.get_advantage(
            user_request=request
        )

        request = DropRequest(
            items=case_data.items,
            state=FoundsState(
                usr_advantage=advantage,
                site_active_hour_funds=1000,  # TODO: Make core services
            ),
            case_price=case_data.price
        )

        dropped = self._service.drop(request=request)

        return self._serializer_class(
            instance={
                "item_id": dropped.dropped_item.id,
                "case_id": case_id
            }
        ).data
