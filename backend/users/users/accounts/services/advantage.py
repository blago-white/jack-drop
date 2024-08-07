from django.db import models

from common.services import BaseService

from ..models.client import Client


class AdvantageService(BaseService):
    default_model = Client

    def update(self, user_id: int, delta_amount: float) -> bool:
        print("ADVANTAGE UPDATE", user_id, delta_amount)

        return self._model.objects.filter(pk=user_id).update(
            advantage=models.F("advantage") + models.Value(delta_amount)
        )
