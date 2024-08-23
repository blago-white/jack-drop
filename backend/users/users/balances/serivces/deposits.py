from django.db import models

from common.services import BaseService

from balances.models import ClientDeposit


class DepositsService(BaseService):
    default_model = ClientDeposit

    def add(self, client_id: int,
            amount: int,
            bonused: float = None
            ) -> models.Model:
        return self._model.objects.create(
            user_id=client_id, amount=amount, bonused=bonused or amount
        )

    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()

    def validate(self, deposit_id: int, amount: int) -> bool:
        return self._model.objects.filter(
            pk=deposit_id,
            amount=amount
        ).exists()
