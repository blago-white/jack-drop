import random

from django.db import models
from rest_framework.exceptions import APIException

from common.services.base import BaseModelService
from .transfer import BattleInfo, BattleMakeRequest, BattleResult, BattlesStats
from ..models import BattleRequest, Battle


class BattleRequestModelService(BaseModelService):
    default_model = BattleRequest

    def create(self, initiator_id: int, battle_case_id: int) -> BattleRequest:
        return self._model.objects.create(
            initiator_id=initiator_id,
            battle_case_id=battle_case_id
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
            dropped_item_loser_id=battle_result.loser_drop.id,
            loser_balance_diff=battle_result.loser_balance_diff,
            winner_balance_diff=battle_result.winner_balance_diff
        )

    def get_stats(self, user_id: int) -> BattlesStats:
        return BattlesStats(
            wins=self._model.objects.filter(winner_id=user_id).count(),
            loses=self._model.objects.filter(loser_id=user_id).count(),
            draw=0
        )

    def get_battles(self, user_id: int) -> models.QuerySet[Battle]:
        return self._model.objects.filter(
            models.Q(winner_id=user_id) | models.Q(loser_id=user_id)
        )


class BattleService:
    def make_battle(self, battle_request: BattleMakeRequest) -> BattleResult:
        case_items = sorted(battle_request.battle_case_items,
                            key=lambda case_item: case_item.price)

        under_price = [i for i in case_items if
                       i.price <= battle_request.battle_case_price]

        print(case_items, battle_request.battle_case_price, battle_request.site_active_funds, "ERRRRR")

        if len(under_price) < 2:
            self._validate_items_price(
                items=case_items[:2],
                case_price=battle_request.battle_case_price,
                active_funds=battle_request.site_active_funds
            )

            under_price = case_items[:2]

        random.shuffle(under_price)

        game_data = list(zip(
            (battle_request.initiator_id, battle_request.participant_id),
            under_price
        ))

        winner, loser = sorted(game_data,
                               reverse=True,
                               key=lambda pair: pair[-1].price)

        winner_b_diff = (
                (winner[-1].price - battle_request.battle_case_price) +
                loser[-1].price
        )

        loser_b_diff = -battle_request.battle_case_price

        return BattleResult(
            battle_info=BattleInfo(
                winner_id=winner[0],
                loser_id=loser[0],
                battle_case_id=battle_request.battle_case_id
            ),
            winner_drop=winner[-1],
            loser_drop=loser[-1],
            winner_balance_diff=winner_b_diff,
            loser_balance_diff=loser_b_diff,
            site_funds_diff=(
                battle_request.battle_case_price - winner[-1].price
            ) + (
                battle_request.battle_case_price - loser[-1].price
            )
        )

    def _validate_items_price(self,
                              items: list,
                              case_price: int,
                              active_funds: float | int) -> None:
        for cip in items:
            if cip.price - case_price > active_funds:
                raise APIException("Case items prices exception")
