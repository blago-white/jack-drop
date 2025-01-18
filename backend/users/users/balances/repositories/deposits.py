from rest_framework.exceptions import ValidationError

from common.repositories import BaseRepository

from accounts.services.advantage import AdvantageService
from balances.serivces.deposits import DepositsService
from balances.serializers import ClientDepositSerializer
from referrals.services.referral import ReferralService
from ..models import ClientDeposit

from promocodes.services.discount import PromocodesService


class DepositRepository(BaseRepository):
    default_service = DepositsService()
    default_promocodes_service = PromocodesService()
    default_advantage_service = AdvantageService()
    default_referrals_service = ReferralService(deposit_model=ClientDeposit)
    default_serializer_class = ClientDepositSerializer

    _service: DepositsService

    def __init__(self, *args,
                 promocodes_service: PromocodesService = None,
                 referrals_service: ReferralService = None,
                 advantage_service: AdvantageService = None,
                 **kwargs):
        self._promocodes_service = promocodes_service or self.default_promocodes_service
        self._referrals_service = referrals_service or self.default_referrals_service
        self._advantage_service = advantage_service or self.default_advantage_service

        super().__init__(*args, **kwargs)

    def create(self, client_id: int, amount: int, promocode: str = None) -> dict:
        serialized = self._serializer_class(
            data={"user_id": client_id, "amount": amount}
        )

        serialized.is_valid(raise_exception=True)

        used_promo = promo_blogger = None

        if promocode:
            discount, used_promo, promo_blogger = self._promocodes_service.use(
                promocode=promocode,
            )

            bonused = amount * (discount / 100)
        else:
            bonused = 0

        created = self._service.add(
            client_id=client_id,
            amount=amount,
            bonused=amount+bonused,
            promocode=used_promo
        )

        if not created:
            raise ValidationError("Error with replenish data", code=400)

        if not promo_blogger:
            to_referr_profit = self._referrals_service.add_referral_deposit(
                referral_id=client_id,
                payed_amount=amount
            )
        else:
            to_referr_profit = self._referrals_service.add_referr_promocode_deposit(
                referr=promo_blogger,
                amount=amount
            )

        self._advantage_service.update(
            user_id=client_id,
            delta_amount=-((bonused - amount) + to_referr_profit)
        )

        result = self._serializer_class(created).data

        result.update({"promocode": promocode})

        return amount+bonused, result

    def validate(self, deposit_id: int, deposit_amount: int) -> dict:
        result = self._service.validate(
            deposit_id=deposit_id,
            amount=deposit_amount
        )

        if not result:
            raise ValidationError("Deposit not found", code=403)

        return {"ok": True}
