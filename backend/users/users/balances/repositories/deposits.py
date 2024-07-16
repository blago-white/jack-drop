from common.repositories import BaseRepository

from balances.serivces.deposits import DepositsService
from balances.serializers import ClientDepositSerializer


class DepositRepository(BaseRepository):
    default_service = DepositsService()
    default_serializer_class = ClientDepositSerializer

    def create(self, client_id: int, amount: int) -> dict:
        return self._serializer_class(self._service.add(
            client_id=client_id,
            amount=amount
        )).data
