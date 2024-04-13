from common.services import BaseService

from ..models.referral import ReferralBenefit


class ReferralService(BaseService):
    default_model = ReferralBenefit

    def get_discount(self, count_referrals) -> int:
        level = self._get_level(count_referrals=count_referrals)
        return level.discount_per_referral

    def _get_level(self, count_referrals) -> ReferralBenefit:
        return self._model.objects.filter(
            count_referrals__lt=count_referrals
        ).order("level").last().level
