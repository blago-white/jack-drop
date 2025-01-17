from django.db import models, transaction

from common.services import BaseService

from ..models.client import Client, ClientAdvantage


class AdvantageService(BaseService):
    default_model = ClientAdvantage
    default_users_model = Client

    def __init__(self, *args, users_model: Client = None, **kwargs):
        self._users_model = users_model or self.default_users_model
        super().__init__(*args, **kwargs)

    @transaction.atomic
    def update(self, user_id: int, delta_amount: float) -> bool:
        print("ADVANTAGE UPDATE", user_id, delta_amount)

        advantage: ClientAdvantage = self._users_model.objects.get(
            pk=user_id
        ).advantage

        advantage.value = models.F("value") + models.Value(delta_amount)

        advantage.save()

        return True

    @transaction.atomic
    def init(self, user: Client):
        if not user.advantage:
            advantage: ClientAdvantage = self._model()

            advantage.save()

            user.advantage = advantage

            user.save()
