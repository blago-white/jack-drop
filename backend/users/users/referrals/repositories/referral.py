from accounts.models import ClientDeposit
from common.repositories import BaseRepository
from referrals.serializers import ReferralStatusSerializer, ReferralLinkSerializer
from referrals.services import referral


class ReferralRepository(BaseRepository):
    default_service = referral.ReferralService(deposit_model=ClientDeposit)
    default_serializer_class = ReferralStatusSerializer

    _service: referral.ReferralService

    def get(self, referral_id):
        data = self._serializer_class(
            data={"referr_id": referral_id,
                  "deposits": self._service.get_deposits_sum(
                      referr_id=referral_id
                  )})

        data.is_valid()

        return data.data


class ReferrRepository(BaseRepository):
    default_service = referral.ReferralService(deposit_model=ClientDeposit)
    default_serializer_class = ReferralLinkSerializer

    def add_referr(self, user_id: int, referr_link: str) -> dict:
        referr = self._service.get_referr_by_link(referr_link=referr_link)

        link_valid = self._service.add_referr(user_id=user_id, referr=referr)

        return ReferralLinkSerializer(instance={
            "referr_link": referr_link,
            "is_valid": link_valid
        }).data
