from django.db.models import Sum, Model

from common.services import BaseService
from ..models.referral import ReferralBenefit, Referral


class ReferralBenefitService(BaseService):
    default_model = ReferralBenefit

    def get_discount(self, deposits_amount: int) -> int:
        level = self.get_level(required_deposits=deposits_amount)
        return level.discount_per_referral

    def get_level(self, required_deposits: int) -> ReferralBenefit:
        return self._model.objects.filter(
            required_deposits__lte=required_deposits
        ).order_by("level").last()


class ReferralService(BaseService):
    default_model = Referral
    _deposits_model: Model

    def __init__(self, deposit_model: Model):
        self._deposits_model = deposit_model

        super().__init__()

    def get_deposits_sum(self, referr_id: int):
        refferals = self._model.objects.filter(
            referr_id=referr_id
        ).values_list("user_id", flat=True)

        deposits = self._deposits_model.objects.filter(
            user_id__in=refferals
        ).aggregate(deposits=Sum("amount")).get("deposits", 0)

        return deposits if deposits is not None else 0

    def update_referral_level(self, referr_id: int):
        deposits = self.get_deposits_sum(referr_id=referr_id)

        level = ReferralBenefitService().get_level(required_deposits=deposits)

        self._model.objects.filter(pk=referr_id).update(benefit=level)

    def create(self, user_id: int,
               referr: int = None,
               benefit: Model = None) -> Model:
        self._model.objects.create(
            user_id=user_id,
            referr=referr,
            benefit=benefit
        )
