from rest_framework.exceptions import ValidationError

from games.api.services.drop import CaseDropApiService
from games.serializers.drop import DropCaseRequestSerializer, DropItemSerializer

from cases.services.items import CaseItemsService

from common.repositories.base import BaseRepository
from .base import BaseApiRepository


class DropItemsRepository(BaseRepository):
    default_service = CaseItemsService()
    default_serializer_class = DropItemSerializer

    def get_drop_items_by_case(self, case_pk: str):
        return self._serializer_class(
            instance=self._service.get_drop_case_items_for_case(
                case_pk=case_pk
            ),
            many=True
        ).data


class CaseDropApiRepository(BaseApiRepository):
    default_endpoint_serializer_class = DropCaseRequestSerializer
    default_api_service = CaseDropApiService()
    _api_service: CaseDropApiService

    def drop(self, user_funds: dict, case_data: dict) -> dict:
        serialized: DropCaseRequestSerializer = (
            self._api_service.default_endpoint_serializer_class(
                data={
                    "case_id": case_data.get("id"),
                    "items": case_data.get("items"),
                    "funds": {
                        "user_advantage": user_funds.get("user_advantage"),
                        "site_active_funds_per_hour": 1000 # TODO: Call service
                    },
                    "price": case_data.get("price")
                }
            )
        )

        serialized.is_valid(raise_exception=True)

        if not self._validate_user_balance(
            balance=user_funds.get("displayed_balance"),
            case_price=serialized.data.get("price")
        ):
            raise ValidationError(
                "There are not enough balance funds for action"
            )

        return {"dropped_item_id": self._api_service.drop(
            serialized=serialized.data
        ).get("item_id")}

    @staticmethod
    def _validate_user_balance(balance: float, case_price: int) -> bool:
        try:
            return float(balance) >= float(case_price)
        except:
            return False
