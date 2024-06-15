from rest_framework.exceptions import ValidationError

from games.api.services.drop import CaseDropApiService
from games.serializers.drop import DropCaseRequestSerializer
from .base import BaseApiService


class CaseDropApiRepository(BaseApiService):
    default_endpoint_serializer_class = DropCaseRequestSerializer
    default_api_service = CaseDropApiService()
    _api_service: CaseDropApiService

    def drop(self, data: dict) -> dict:
        serialized: DropCaseRequestSerializer = (
            self._api_service.default_endpoint_serializer_class(
                data=data
            )
        )

        serialized.is_valid(raise_exception=True)

        if not self._validate_user_balance(
            balance=data.get("displayed_balance"),
            case_price=data.get("price")
        ):
            raise ValidationError(
                "There are not enough balance funds for action"
            )

        return {"dropped": self._api_service.drop(
            serialized=serialized.data
        )}

    @staticmethod
    def _validate_user_balance(balance: float, case_price: int) -> bool:
        try:
            return balance >= case_price
        except:
            return False
