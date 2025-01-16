from django.db import models

from accounts.models import Client
from ..models import Promocode, PromocodeActivation

from common.services import BaseService


class PromocodesService(BaseService):
    default_model = Promocode

    def get_discount(self, promocode: str) -> int:
        try:
            promo = self._model.objects.get(code=promocode)

            return promo.discount if promo.usages else 0
        except:
            return 0

    def use(self, promocode: str) -> tuple[int, Promocode | None]:
        try:
            promo = self._model.objects.get(code=promocode)

            if not promo.usages:
                raise ValueError
        except:
            return 0, None

        if not int(promo.usages) <= -1:
            promo.usages = models.F("usages") - 1

        promo.save()

        return promo.discount, promo
