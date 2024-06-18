from django.db import models

from common.services.base import BaseService

from ..models import FrozenSiteProfit


class FrozenFundsService(BaseService):
    default_model = FrozenSiteProfit
    _model: FrozenSiteProfit

    def update(self, delta_funds: float | int) -> float | int:
        self._get_row().update(
            amount=models.F("amount") + delta_funds
        )

    def _get_row(self) -> models.QuerySet[FrozenSiteProfit]:
        return self._model.objects.all()
