from django.db import models

from common.services.base import BaseService

from ..models import CasesDropsProfit


class CasesProfitService(BaseService):
    default_model = CasesDropsProfit

    def get(self) -> float:
        return self._model.objects.first().amount

    def update(self, delta_funds: float):
        profit = self._model.objects.first()

        profit.amount = models.F("amount") + delta_funds
        profit.amount_updated = True

        profit.save()

    def drop_profit(self):
        profit = self._model.objects.first()

        if not profit.amount_updated:
            return

        profit.amount = models.F("amount") * 0.5
        profit.amount_updated = False

        profit.save()
