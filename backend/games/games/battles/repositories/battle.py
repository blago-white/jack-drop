from common.repositories import BaseRepository

from battles.services.transfer import BattleMakeRequest, BattleResult
from battles.services.battle import (BattleRequestModelService,
                                     BattleModelService, BattleService)
from battles.serializers import BattleRequestSerializer, BattleSerializer, MakeBattleSerializer
from battles.services.transfer import BattleInfo


class BattleRequestRepository(BaseRepository):
    default_service = BattleRequestModelService()
    default_serializer_class = BattleRequestSerializer

    _service: BattleRequestModelService

    def create(self, request_data: dict) -> dict:
        serialized: BattleRequestSerializer = self._serializer_class(
            data=request_data
        )

        serialized.is_valid(raise_exception=True)

        instance = self._service.create(
            initiator_id=serialized.get("initiator_id"),
            case_id=serialized.get("case_id")
        )

        return {"ok": instance is not None}

    def drop(self, initiator_id: int) -> dict:
        result = self._service.cancel(initiator_id=initiator_id)

        return {"ok": result}


class BattleRepository(BaseRepository):
    default_service = BattleModelService()
    default_battle_request_service = BattleRequestModelService()
    default_game_service = BattleService()

    default_serializer_class = MakeBattleSerializer

    _service: BattleModelService
    _game_service: BattleService
    _battle_request_service: BattleRequestModelService

    def make(self, request_data: dict) -> dict:
        serialized: MakeBattleSerializer = self._serializer_class(
            data=request_data
        )

        serialized.is_valid(raise_exception=True)

        self._validate_initiator(validated=serialized)

        self._battle_request_service.cancel(initiator_id=serialized.data.get(
            "initiator_id"
        ))

        result = self._game_service.make_battle(
            battle_request=self._serialize_make_battle_request(
                serialized=serialized
            )
        )

        return self._serializer_class(
            instance=self._commit_result(instance=result)
        ).data

    def _commit_result(self, instance: BattleResult) -> object:
        return self._service.create(battle_result=instance)

    def _validate_initiator(self, validated: MakeBattleSerializer) -> bool:
        return self._battle_request_service.is_initiator(
            initiator_id=validated.validated_data.get("initiator_id")
        )

    @staticmethod
    def _serialize_make_battle_request(serialized: dict) -> BattleMakeRequest:
        return BattleMakeRequest(
            initiator_id=serialized.data.get("initiator_id"),
            participant_id=serialized.data.get("initiator_id"),
            battle_case_id=serialized.data.get("battle_case_id"),
            battle_case_price=serialized.data.get("battle_case_price"),
            battle_case_items=serialized.data.get("battle_case_items"),
            site_active_hour_funds=serialized.data.get(
                "site_funds"
            ).get("site_active_hour_funds"),
        )
