from rest_framework.exceptions import ValidationError

from common.repositories import BaseRepository

from balances.serivces.deposits import DepositsService
from balances.serializers import ClientDepositSerializer

from promocodes.services.discount import PromocodesService


class DepositRepository(BaseRepository):
    default_service = DepositsService()
    default_promocodes_service = PromocodesService()
    default_serializer_class = ClientDepositSerializer

    _service: DepositsService

    def __init__(self, *args,
                 promocodes_service: PromocodesService = None,
                 **kwargs):
        self._promocodes_service = promocodes_service or self.default_promocodes_service

        super().__init__(*args, **kwargs)

    def create(self, client_id: int, amount: int, promocode: str = None) -> dict:
        serialized = self._serializer_class(
            data={"user_id": client_id, "amount": amount}
        )

        serialized.is_valid(raise_exception=True)

        if promocode:
            bonused = amount * self._promocodes_service.use(
                promocode=promocode,
                client_id=client_id
            ) / 100
        else:
            bonused = 0

        created = self._service.add(
            client_id=client_id,
            amount=amount+bonused,
            bonused=bonused
        )

        if not created:
            raise ValidationError("Error with replenish data", code=400)

        result = self._serializer_class(created).data

        result.update({"promocode": promocode})

        return result

    def validate(self, deposit_id: int, deposit_amount: int) -> dict:
        result = self._service.validate(
            deposit_id=deposit_id,
            amount=deposit_amount
        )

        if not result:
            raise ValidationError("Deposit not found", code=403)

        return {"ok": True}
