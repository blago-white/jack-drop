from django.db import models

from common.services.base import BaseService

from ..models import DinamicSiteProfit


class DinamicFundsService(BaseService):
    default_model = DinamicSiteProfit
    _model: DinamicSiteProfit

    def update(self, delta_funds: float | int) -> float | int:
        if (self.get() + delta_funds) < self.get_min_value():
            return self.get()

        self._get_row().update(
            amount=models.F("amount") + delta_funds
        )

        return self.get()

    def get(self) -> float | int:
        return self._get_row().first().amount

    def get_min_value(self) -> float | int:
        return self._get_row().first().min_value

    def _get_row(self) -> models.QuerySet[DinamicSiteProfit]:
        return self._model.objects.all()
