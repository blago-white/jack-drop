from rest_framework.exceptions import ValidationError

from common.repositories import BaseRepository

from balances.serivces.deposits import DepositsService
from balances.serializers import ClientDepositSerializer


class DepositRepository(BaseRepository):
    default_service = DepositsService()
    default_serializer_class = ClientDepositSerializer

    _service: DepositsService

    def create(self, client_id: int, amount: int) -> dict:
        serialized = self._serializer_class(
            data={"user_id": client_id, "amount": amount}
        )

        serialized.is_valid(raise_exception=True)

        created = self._service.add(
            client_id=client_id,
            amount=amount
        )

        if not created:
            raise ValidationError("Error with replenish data", code=400)

        return self._serializer_class(created).data

    def validate(self, deposit_id: int, deposit_amount: int) -> dict:
        result = self._service.validate(
            deposit_id=deposit_id,
            amount=deposit_amount
        )

        if not result:
            raise ValidationError("Deposit not found", code=403)

        return {"ok": True}
