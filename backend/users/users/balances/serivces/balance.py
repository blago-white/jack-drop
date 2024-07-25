from django.db.models import F, Value
from django.core.exceptions import ValidationError

from common.services import BaseService

from ..models import ClientBalance


class ClientBalanceService(BaseService):
    default_model = ClientBalance

    def get_real_balance(self, client_id: int) -> float:
        return self.get_balance(client_id=client_id).real_balance

    def get_displayed_balance(self, client_id: int) -> float:
        return self.get_balance(client_id=client_id).displayed_balance

    def get_balance(self, client_id: int) -> ClientBalance:
        return self._model.objects.get(client_id=client_id)

    def udpdate_displayed_balance(self, client_id: int,
                                  delta_balance: float) -> bool:
        print("UPDATE", client_id, delta_balance)

        current = self.get_balance(client_id=client_id)

        if (current.displayed_balance + delta_balance < 0) and (delta_balance < 0):
            raise ValidationError("Not correct data for update")

        return self._model.objects.filter(client_id=client_id).update(
            displayed_balance=F("displayed_balance") + Value(delta_balance)
        ) > 0

    def update_real_balance(self, client_id: int,
                            delta_balance: float) -> bool:
        return self._model.objects.filter(client_id=client_id).update(
            real_balance=F("real_balance") + Value(delta_balance)
        )

    def create(self, client_id: int) -> bool:
        return bool(
            self._model.objects.create(client_id=client_id)
        )
