import random

from rest_framework.exceptions import APIException

from common.services.base import BaseModelService

from ..models import BattleRequest, Battle
from .transfer import BattleInfo, BattleMakeRequest, BattleResult
from common.services.api.states import FundsState
from cases.services.drop import CaseItemDropModelService


class BattleRequestModelService(BaseModelService):
    default_model = BattleMakeRequest

    def create(self, initiator_id: int, case_id: int) -> BattleMakeRequest:
        return self._model.objects.create(
            initiator_id=initiator_id,
            case_id=case_id
        )

    def cancel(self, initiator_id: int) -> bool:
        return bool(
            self._model.objects.filter(initiator_id=initiator_id).delete()
        )

    def is_initiator(self, initiator_id: int) -> bool:
        return self._model.objects.filter(initiator_id=initiator_id).exists()


class BattleModelService(BaseModelService):
    default_model = Battle

    def create(self, battle_result: BattleResult) -> Battle:
        return self._model.objects.create(
            winner_id=battle_result.battle_info.winner_id,
            loser_id=battle_result.battle_info.loser_id,
            battle_case_id=battle_result.battle_info.battle_case_id,
            dropped_item_winner_id=battle_result.winner_drop.id,
            dropped_item_loser_id=battle_result.loser_drop.id
        )


class BattleService:
    def make_battle(self, battle_request: BattleMakeRequest) -> BattleResult:
        case_items = sorted(battle_request.battle_case_items,
                            key=lambda case_item: case_item.price)

        under_price = [i for i in case_items if
                       i.price <= battle_request.battle_case_price]

        if len(under_price) < 2:
            self._validate_items_price(
                items=case_items[:2],
                case_price=battle_request.battle_case_price,
                active_funds=battle_request.site_active_hour_funds
            )

            under_price = case_items[:2]

        random.shuffle(under_price)

        game_data = list(zip(
            (battle_request.initiator_id, battle_request.participant_id),
            under_price
        ))

        winner, loser = sorted(game_data,
                               reverse=True,
                               key=lambda pair: pait[-1].price)

        return BattleResult(
            battle_info=BattleInfo(
                winner_id=winner[0],
                loser_id=loser[0],
                battle_case_id=battle_request.battle_case_id
            ),
            winner_drop=winner[-1],
            loser_drop=loser[-1]
        )

    def _validate_items_price(self,
                              items: BattleMakeRequest.battle_case_items,
                              case_price: int,
                              active_funds: float | int) -> None:
        for cip in items:
            if cip - case_price > active_funds:
                raise APIException("Case items prices exception")
