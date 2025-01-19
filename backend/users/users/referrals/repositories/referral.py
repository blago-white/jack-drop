from rest_framework.exceptions import ValidationError

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
        referral_ = self._service.get_profile(referral_id=referral_id)

        if not referral_.is_blogger:
            raise ValidationError("You is not blogger")

        count_referrals = self._service.get_referrals_count(referral=referral_)

        data = self._serializer_class(
            data={"referr_id": referral_id,
                  "profit": referral_.referrals_loses_funds,
                  "reflink": referral_.full_refer_link,
                  "total_deposits": (referral_.referrals_loses_funds /
                                     referral_.benefit_percent)*100,
                  "count_referrals": count_referrals})

        data.is_valid()

        print(self._service.get_deposits_sum(referr_id=referral_id))

        print(f"REF STATUS {data.data=}")

        return data.data


class ReferrRepository(BaseRepository):
    default_service = referral.ReferralService(deposit_model=ClientDeposit)
    default_serializer_class = ReferralLinkSerializer

    _service: referral.ReferralService

    def add_referr(self, user_id: int, referr_link: str) -> dict:
        referr = self._service.get_referr_by_link(referr_link=referr_link)

        if not referr:
            return ReferralLinkSerializer(instance={
                "referr_link": referr_link,
                "is_valid": False
            }).data

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
