from django.db.models import Sum, Model

from common.services import BaseService
from ..models.referral import Referral


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

    def user_exists(self, user_id: int) -> bool:
        return self._model.objects.filter(user_id=user_id).exists()

    def create(self, user_id: int,
               referr: int = None,
               is_blogger: Model = False) -> Model:
        self._model.objects.create(
            user_id=user_id,
            referr=referr,
            is_blogger=is_blogger
        )

    def add_referr(self, user_id: int, referr: Model) -> bool:
        return bool(self._model.objects.filter(
            user_id=user_id, referr_id=None
        ).update(referr_id=referr.pk))

    def get_referr_by_link(self, referr_link: str) -> Model:
        return self._model.objects.filter(referr_link=referr_link).first()

    def get_profile(self, referral_id: int) -> Referral:
        return self._model.objects.get(user_id=referral_id)

    def add_user_lose(self, user_id: int, delta_funds: float) -> Referral:
        referral = self._model.objects.get(user_id=user_id)
        referr: Referral = referral.referr

        if referr.is_blogger:
            referr.referrals_loses_funds += delta_funds * .2

            referr.save()

            return referr, delta_funds * .8

        return referr, delta_funds
