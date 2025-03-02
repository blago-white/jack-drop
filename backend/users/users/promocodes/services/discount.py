from django.db import models

from accounts.models import Client
from referrals.models.referral import Referral

from ..models import Promocode, PromocodeActivation

from common.services import BaseService


class PromocodesService(BaseService):
    default_model = Promocode

    def get_discount(self, promocode: str) -> int:
        try:
            promo = self._model.objects.get(code=promocode)

            return promo.discount if promo.usages else 0
        except Exception as e:
            print(e)
            return 0

    def get_for_personal_offer(self) -> Promocode:
        try:
            return self._model.objects.filter(for_personal_offers=True).first()
        except:
            return False

    def use(self, promocode: str) -> tuple[
        int, Promocode | None, Referral | None
    ]:
        try:
            promo: Promocode = self._model.objects.get(code=promocode)

            if not promo.usages:
                raise ValueError

            if promo.for_personal_offers:
                pass
        except:
            return 0, None, None

        if not int(promo.usages) <= -1:
            promo.usages = models.F("usages") - 1

        promo.save()

        return promo.discount, promo, promo.blogger
