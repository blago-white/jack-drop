from balances.models import ClientDeposit
from common.repositories import BaseRepository
from referrals.serializers import ReferralStatusSerializer, ReferralLinkSerializer
from referrals.services import referral
from referrals.models.referral import Referral


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

    _service: referral.ReferralService

    def add_referr(self, user_id: int, referr_link: str) -> dict:
        referr = self._service.get_referr_by_link(referr_link=referr_link)

        link_valid = self._service.add_referr(user_id=user_id, referr=referr)

        return ReferralLinkSerializer(instance={
            "referr_link": referr_link,
            "is_valid": link_valid
        }).data

    def add_referr_funds(self, referral_id: int, advantage_diff: float) -> dict:
        referr: Referral = self._service.get_profile(referral_id=referral_id).referr

        if referr.is_blogger and advantage_diff < 0:
            referr = self._service.add_funds(
                referr=referr,
                delta_funds=abs(advantage_diff * .2)
            )

            return {"ok": True, "user_advantage": advantage_diff * .8}

        return {"ok": True, "user_advantage": advantage_diff}
