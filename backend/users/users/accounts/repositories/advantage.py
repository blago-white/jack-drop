from common.repositories import BaseRepository
from referrals.services.referral import ReferralService
from balances.models import ClientDeposit
from ..serializers import UpdateAdvantageSerializer
from ..services.advantage import AdvantageService


class AdvantageRepository(BaseRepository):
    default_service = AdvantageService()

    default_referral_service = ReferralService(deposit_model=ClientDeposit)
    default_serializer_class = UpdateAdvantageSerializer

    def update(self, user_id: int, delta_amount: float):
        referr, remains = self.default_referral_service.add_funds(
            referr=user_id,
            delta_funds=delta_amount
        )

        return {
            "ok": self._service.update(
                user_id=user_id, delta_amount=remains
            )
        }
