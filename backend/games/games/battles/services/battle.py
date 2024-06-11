from common.services.base import BaseModelService

from ..models import BattleRequest, Battle
from .transfer import BattleInfo
from common.services.api.states import FundsState


class BattleRequestModelService(BaseModelService):
    default_model = BattleRequest

    def create(self, initiator_id: int, case_id: int) -> BattleRequest:
        return self._model.objects.create(
            initiator_id=initiator_id,
            case_id=case_id
        )

    def cancel(self, initiator_id: int) -> bool:
        return bool(
            self._model.objects.filter(initiator_id=initiator_id).delete()
        )


class BattleModelService(BaseModelService):
    default_model = Battle

    def __init__(self,
                 battle_request_service=BattleRequestModelService(),
                 **kwargs):
        self._battle_request_service = battle_request_service

        super().__init__(**kwargs)

    def create(self, battle_request: BattleRequest,
               battle_info: BattleInfo) -> Battle:
        self._battle_request_service.cancel(
            initiator_id=battle_request.initiator_id
        )

        return self._model.objects.create(
            winner_id=battle_info.winner_id,
            loser_id=battle_info.loser_id,
            battle_case_id=battle_info.battle_case_id,
        )


class BattleService:
    def make_battle(self, ):
        return
