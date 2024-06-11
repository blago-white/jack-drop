from rest_framework.exceptions import ValidationError

from .base import BaseApiRepository

from cases.services.cases import CaseService
from games.api.services.battle import BattleRequestApiService
from games.serializers.battle import BattleRequestServiceEndpointSerializer


class BattleRequestApiRepository(BaseApiRepository):
    default_api_service = BattleRequestApiService()
    default_cases_service = CaseService()

    _api_service: BattleRequestApiService

    def __init__(self, *args,
                 cases_service: CaseService = None,
                 **kwargs):
        self._cases_service = cases_service or self.default_cases_service

        super().__init__(*args, **kwargs)

    def create(self, battle_case_id: int,
               user_data: dict) -> dict:
        serialized: BattleRequestServiceEndpointSerializer = (
            self.default_api_service.default_endpoint_serializer_class(
                data={
                    "battle_case_id": battle_case_id,
                    "initiator_id": user_data.get("id")
                }
            )
        )

        serialized.is_valid(raise_exception=True)

        self._validate_funds(battle_case_id=battle_case_id,
                             user_data=user_data)

        ok = self._api_service.create(serialized=serialized)

        return {"ok": ok}

    def _validate_funds(self, battle_case_id: int, user_data: dict) -> None:
        case_price = self._cases_service.get_price(case_id=battle_case_id)

        if user_data.get("displayed_balance") < case_price:
            raise ValidationError(
                "There are not enough balance funds for action"
            )


class BattleApiRepository(BaseApiRepository):
    default_api_service = BattleRequestApiService()
    default_cases_service = CaseService()

    _api_service: BattleRequestApiService

    def __init__(self, *args,
                 cases_service: CaseService = None,
                 **kwargs):
        self._cases_service = cases_service or self.default_cases_service

        super().__init__(*args, **kwargs)

    def make(self, battle_case_id: int,
             user_data: dict) -> dict:
        pass
