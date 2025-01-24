from django.db.models import Sum, Model, F, Value, Q

from common.services import BaseService
from promocodes.models import Promocode

from ..models.referral import Referral


class ReferralService(BaseService):
    default_model = Referral
    _promocodes_model = Promocode
    _deposits_model: Model

    def __init__(self, deposit_model: Model,
                 promocodes_model: Promocode = None):
        self._deposits_model = deposit_model
        self._promocodes_model = promocodes_model or self._promocodes_model

        super().__init__()

    def get_deposits_stat(self, referr_id: int) -> tuple[float, int]:
        """
        :return: tuple of two values, first - sum of deposits, second - count
        """

        refferals_ids = self._model.objects.filter(
            referr_id=referr_id
        ).values_list("user_id", flat=True)

        referr_promocodes = self._promocodes_model.objects.filter(
            blogger_id=referr_id
        ).values_list("id", flat=True)

        deposits = self._deposits_model.objects.filter(
            Q(user_id__in=refferals_ids) |
            Q(promocode_id__in=referr_promocodes)
        ).aggregate(deposits=Sum("amount")).get("deposits", 0)

        promocodes_usages = self._deposits_model.objects.filter(
            promocode_id__in=referr_promocodes
        ).count()

        return (0 or deposits), promocodes_usages

    def get_referrals_count(self, referral: Referral):
        return self._model.objects.filter(referr=referral).count() 

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

        if referr and referr.is_blogger:
            referr.referrals_loses_funds += abs(delta_funds) * .2

            referr.save()

            return referr, abs(delta_funds) * .2

        return referr, 0

    def add_referral_deposit(self, referral_id: int, payed_amount: float | int):
        referr: Referral = self.get_profile(
            referral_id=referral_id
        ).referr

        if referr:
            referr_profit = payed_amount * (referr.benefit_percent / 100)

            referr.referrals_loses_funds = F("referrals_loses_funds") + Value(
                referr_profit
            )

            referr.save()

            return referr_profit
        
        return 0

    @staticmethod
    def add_referr_promocode_deposit(referr: Referral,
                                     amount: float) -> float:
        discount = referr.benefit_percent / 100

        referr.referrals_loses_funds = F("referrals_loses_funds") + (
            amount * discount
        )

        referr.save()

        return amount * discount
