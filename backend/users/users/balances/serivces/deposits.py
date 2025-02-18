from django.db import models

from common.services import BaseService

from balances.models import ClientDeposit

from promocodes.models import Promocode


class DepositsService(BaseService):
    default_model = ClientDeposit

    def add(self, client_id: int,
            amount: int,
            bonused: float = None,
            promocode: Promocode = None
            ) -> models.Model:
        return self._model.objects.create(
            user_id=client_id,
            amount=amount,
            bonused=bonused or amount,
            promocode=promocode
        )

    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()

    def validate(self, deposit_id: int, amount: int) -> bool:
        return self._model.objects.filter(
            pk=deposit_id,
            amount=amount
        ).exists()

    def has_deposits(self, user_id: int) -> bool:
        return self._model.objects.filter(
            user_id=user_id
        ).exists()
