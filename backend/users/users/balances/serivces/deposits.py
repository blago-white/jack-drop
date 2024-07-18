from django.db import models

from common.services import BaseService

from balances.models import ClientDeposit


class DepositsService(BaseService):
    default_model = ClientDeposit

    def add(self, client_id: int, amount: int) -> models.Model:
        return self._model.objects.create(
            user_id=client_id, amount=amount
        )

    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()
