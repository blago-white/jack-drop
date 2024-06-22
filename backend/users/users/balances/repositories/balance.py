from common.repositories import BaseRepository

from ..serivces.balance import ClientBalanceService
from ..serializers import ClientBalanceSerializer


class BalanceRepository(BaseRepository):
    default_service = ClientBalanceService()

    default_serializer_class = ClientBalanceSerializer

    _service: ClientBalanceService

    def get_displayed_balance(self, client_id: int) -> dict:
        balance = self._service.get_displayed_balance(client_id=client_id)

        return {"balance": balance}

    def update_displayed_balance(self, client_id: int,
                                 delta_amount: float) -> dict:
        result = self._service.udpdate_displayed_balance(
            client_id=client_id,
            delta_balance=delta_amount
        )

        return {"ok": result}

    def update_hidden_balance(self, client_id: int,
                              delta_amount: float) -> dict:
        result = self._service.update_real_balance(client_id=client_id,
                                                   delta_balance=delta_amount)

        return {"ok": result}
