from django.db import models, transaction

from common.services.base import BaseService

from ..models import CasesDropsProfit


class CasesProfitService(BaseService):
    default_model = CasesDropsProfit

    def get(self) -> float:
        return self._model.objects.first().amount

    @transaction.atomic()
    def update(self, delta_funds: float):
        profit = self._model.objects.first()

        profit.amount_updated = True

        if delta_funds > 0:
            delta_funds *= .6

        profit.amount = models.F("amount") + delta_funds

        profit.save()

    @transaction.atomic()
    def drop_profit(self):
        profit = self._model.objects.first()

        if not profit.amount_updated:
            return

        if profit.amount:
            profit.amount = models.F("amount") * 0.5

        profit.amount_updated = False

        profit.save()
