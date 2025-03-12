from django.db import models

from common.services import BaseService

from ..models.client import LotteryWin
from .transfer import LotteryResult, LotteryPrize


class LotteryWinsModelService(BaseService):
    default_model = LotteryWin

    def add(self, result: LotteryResult):
        if not result.prizes:
            return

        wins = [
            LotteryWin(
                winner_id=prize.winner_id,
                prize_item_id=prize.prize_item_id
            ) for prize in result.prizes
        ]

        self._model.objects.bulk_create(wins)

    def retrieve_list_unviewed_prizes(self, client_id: int) -> list[LotteryWin]:
        unviewed = self._get_unviewed(client_id=client_id)

        self._mark_viewed(unviewed_qs=unviewed)

        return list(unviewed.values("prize_item_id"))

    def _mark_viewed(self, unviewed_qs: models.QuerySet):
        unviewed_qs.update(viewed=True)

    def _get_unviewed(self, client_id: int):
        return self._model.objects.filter(
            winner_id=client_id,
            viewed=False
        )
