from rest_framework.request import Request

from common.repositories import BaseRepository
from common.services.api.states import FundsState
from ..serializers import DropCaseRequestSerializer, DropResultSerializer
from ..services.drop import CaseItemDropService, CaseItemDropModelService
from ..states.request import DropRequest, DetailedCaseItem


class CaseItemDropRepository(BaseRepository):
    default_service = CaseItemDropService()
    default_serializer_class = DropCaseRequestSerializer
    _result_serializer_class: DropResultSerializer
    _drop_model_service: CaseItemDropModelService
    _service: CaseItemDropService

    def __init__(self, *args,
                 result_serializer_class: DropResultSerializer =
                 DropResultSerializer,
                 drop_model_service: CaseItemDropModelService = CaseItemDropModelService(),
                 **kwargs):
        self._result_serializer_class = result_serializer_class
        self._drop_model_service = drop_model_service

        super().__init__(*args, **kwargs)

    def drop_item(self, request: Request) -> dict:
        drop_request_data: DropCaseRequestSerializer = self._serializer_class(
            data=request.data
        )

        drop_request_data.is_valid(raise_exception=True)

        request = self._serialize_drop_request(data_json=drop_request_data)
        dropped = self._service.drop(request=request)

        self._drop_model_service.add(
            user_id=drop_request_data.data.get("user_id"),
            result=dropped
        )

        return self._result_serializer_class(
            instance={
                "item": dropped.dropped_item,
                "funds": {
                    "user_funds_delta": dropped.user_funds_delta,
                    "site_funds_delta": dropped.site_funds_delta
                }
            }
        ).data

    def _serialize_drop_request(self, data_json: dict) -> DropRequest:
        return DropRequest(
            items=[
                DetailedCaseItem(
                    id=i.get("id"),
                    item_id=i.get("item_id"),
                    price=i.get("price"),
                    rate=i.get("rate"),
                    title=i.get("title"),
                    image_path=i.get("image_path")
                ) for i in data_json.data.get("items")
            ],
            state=FundsState(
                usr_advantage=data_json.data.get("funds").get(
                    "user_advantage"
                ),
                site_active_funds=data_json.data.get("funds").get(
                    "site_active_funds"
                ),
            ),
            case_price=data_json.data.get("price"),
            early_drops_rate=self._drop_model_service.get_early_games_rate(
                user_id=data_json.data.get("user_id")
            )
        )
