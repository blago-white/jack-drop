from common.services import BaseService

from ..models import ClientBalance


class ClientBalanceService(BaseService):
    default_model = ClientBalance

    def get_real_balance(self, client_id: int) -> float:
        return self.get_balance(client_id=client_id).real_balance

    def get_displayed_balance(self, client_id: int) -> float:
        return self.get_balance(client_id=client_id).displayed_balance

    def get_balance(self, client_id: int) -> ClientBalance:
        return self._model.objects.get(pk=client_id)
