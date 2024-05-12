from accounts.models import ClientDeposit
from common.repositories import BaseRepository
from referrals.serializers import ReferralStatusSerializer
from referrals.services import referral


class ReferralRepository(BaseRepository):
    default_service = referral.ReferralService(deposit_model=ClientDeposit)
    default_serializer_class = ReferralStatusSerializer

    def get(self, referral_id):
        data = self._serializer_class(
            data={"referr_id": referral_id,
                  "deposits": self._service.get_deposits_sum(
                      referr_id=referral_id
                  )})

        data.is_valid()

        return data.validated_data
