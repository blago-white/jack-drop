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
