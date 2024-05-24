from common.services.base import BaseModelService

from ..models import BattleRequest, Battle
from .transfer import BattleInfo


class BattleRequestService(BaseModelService):
    default_model = BattleRequest

    def create(self, initiator_id: int, case_id: int) -> BattleRequest:
        return self._model.objects.create(
            initiator_id=initiator_id,
            case_id=case_id
        )

    def drop(self, initiator_id: int) -> bool:
        return bool(
            self._model.objects.filter(initiator_id=initiator_id).delete()
        )


class BattleService(BaseModelService):
    default_model = Battle

    def create(self, battle_info: BattleInfo) -> Battle:
        return self._model.objects.create(
            winner_id=battle_info.winner_id,
            loser_id=battle_info.loser_id,
            battle_case_id=battle_info.battle_case_id,
        )
