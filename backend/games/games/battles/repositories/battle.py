from rest_framework.exceptions import ValidationError
from django.forms.models import model_to_dict

from common.repositories import BaseRepository

from battles.services.transfer import BattleMakeRequest, BattleResult, CaseItem
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
            initiator_id=serialized.data.get("initiator_id"),
            battle_case_id=serialized.data.get("battle_case_id")
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
    default_battle_serializer_class = BattleSerializer

    _service: BattleModelService
    _game_service: BattleService
    _battle_request_service: BattleRequestModelService
    _battle_serializer_class: BattleSerializer

    def __init__(self, *args,
                 battle_request_service: BattleRequestModelService = None,
                 game_service: BattleService = None,
                 battle_serializer_class: BattleSerializer = None,
                 **kwargs):
        self._battle_request_service = battle_request_service or self.default_battle_request_service
        self._game_service = game_service or self.default_game_service
        self._battle_serializer_class = (battle_serializer_class or
                                         self.default_battle_serializer_class)

        super().__init__(*args, **kwargs)

    def make(self, request_data: dict) -> dict:
        serialized: MakeBattleSerializer = self._serializer_class(
            data=request_data
        )

        serialized.is_valid(raise_exception=True)

        self._validate_initiator(validated=serialized)

        result = self._game_service.make_battle(
            battle_request=self._serialize_make_battle_request(
                serialized=serialized
            )
        )

        self._battle_request_service.cancel(initiator_id=serialized.data.get(
            "initiator_id"
        ))

        return self._battle_serializer_class(
            instance=model_to_dict(
                self._commit_result(instance=result)
            ) | {"site_funds_diff": result.site_funds_diff}
        ).data

    def _commit_result(self, instance: BattleResult) -> object:
        return self._service.create(battle_result=instance)

    def _validate_initiator(self, validated: MakeBattleSerializer) -> bool:
        if not self._battle_request_service.is_initiator(
            initiator_id=validated.validated_data.get("initiator_id")
        ):
            raise ValidationError(
                "Battle request not found",
                code=400
            )

        if (validated.validated_data.get("participant_id") ==
                validated.validated_data.get("initiator_id")):
            raise ValidationError(
                "Battle initiator is participant",
                code=400
            )

    @staticmethod
    def _serialize_make_battle_request(serialized: dict) -> BattleMakeRequest:
        return BattleMakeRequest(
            initiator_id=serialized.data.get("initiator_id"),
            participant_id=serialized.data.get("participant_id"),
            battle_case_id=serialized.data.get("battle_case_id"),
            battle_case_price=serialized.data.get("battle_case_price"),
            battle_case_items=[
                CaseItem(id=item.get("id"),
                         price=item.get("price"),
                         rate=item.get("rate"))
                for item in serialized.data.get("battle_case_items")
            ],
            site_active_funds=serialized.data.get(
                "site_funds"
            ).get("site_active_funds"),
        )
