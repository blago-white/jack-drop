from rest_framework.exceptions import ValidationError

from cases.services.cases import CaseService
from cases.services.items import CaseItemsService

from games.api.services.battle import BattleRequestApiService, BattleApiService
from games.serializers.battle import BattleRequestServiceEndpointSerializer
from games.serializers.drop import DropItemSerializer

from .base import BaseApiRepository


class _BaseBattleApiRepository(BaseApiRepository):
    def _validate_funds(self, battle_case_id: int, user_data: dict) -> None:
        case_price = self._cases_service.get_price(case_id=battle_case_id)

        if user_data.get("displayed_balance") < case_price:
            raise ValidationError(
                "There are not enough balance funds for action"
            )


class BattleRequestApiRepository(_BaseBattleApiRepository):
    default_api_service = BattleRequestApiService()
    default_cases_service = CaseService()

    _api_service: BattleRequestApiService

    def __init__(
            self, *args,
            cases_service: CaseService = None,
            **kwargs):
        self._cases_service = cases_service or self.default_cases_service

        super().__init__(*args, **kwargs)

    def create(
            self, battle_case_id: int,
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

    def cancel(self, initiator_id: int) -> dict:
        ok = self._api_service.cancel(initiator_id=initiator_id)

        return {"ok": ok}


class BattleApiRepository(_BaseBattleApiRepository):
    default_cases_service = CaseService()
    default_api_service = BattleApiService()
    default_case_items_service = CaseItemsService()

    _api_service: BattleApiService

    def __init__(
            self, *args,
            cases_service: CaseService = None,
            case_items_service: CaseItemsService = None,
            **kwargs):
        self._cases_service = cases_service or self.default_cases_service
        self._case_items_service = (case_items_service or
                                    self.default_case_items_service)

        super().__init__(*args, **kwargs)

    def make(
            self, battle_case_id: int,
            initiator_id: int,
            participant_id: int) -> dict:
        case_data = self._cases_service.get(
            case_id=battle_case_id
        )

        serialized = self._api_service.default_endpoint_serializer_class(
            data={
                "initiator_id": initiator_id,
                "participant_id": participant_id,
                "site_funds": {
                    "site_active_funds_per_hour": 1000,  # TODO: Call ervice
                },
                "battle_case_id": case_data.pk,
                "battle_case_price": case_data.price,
                "battle_case_items": DropItemSerializer(
                    instance=self._case_items_service.get_drop_case_items_for_case(
                        case_pk=case_data.pk
                    ),
                    many=True
                ).data
            }
        )

        serialized.is_valid(raise_exception=True)

        return self._api_service.make(
            serialized=serialized
        )
