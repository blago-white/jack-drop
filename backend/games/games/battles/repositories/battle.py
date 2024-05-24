from common.repositories import BaseRepository

from battles.services.battle import BattleRequestService, BattleService
from battles.serializers import BattleRequestSerializer, BattleSerializer
from battles.services.transfer import BattleInfo


class BattleRequestRepository(BaseRepository):
    default_service = BattleRequestService()
    default_serializer_class = BattleRequestSerializer

    _service: BattleRequestService

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
        result = self._service.drop(initiator_id=initiator_id)

        return {"ok": result}


class BattleRepository(BaseRepository):
    default_service = BattleService()
    default_serializer_class = BattleSerializer

    _service: BattleService

    def create(self, request_data: dict) -> dict:
        serialized: BattleSerializer = self._serializer_class(data=request_data)

        serialized.is_valid(raise_exception=True)

        created = self._service.create(battle_info=BattleInfo(
            *serialized.validated_data
        ))

        return self._serializer_class(instance=created).data
