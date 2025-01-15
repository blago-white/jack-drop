from django.db import models

from accounts.models import Client
from ..models import Promocode, PromocodeActivation

from common.services import BaseService


class PromocodesService(BaseService):
    default_model = Promocode
    default_activation_model = PromocodeActivation

    def __init__(self, *args,
                 activation_model: models.Model = None,
                 **kwargs):
        self._activation_model = activation_model or self.default_activation_model

        super().__init__(*args, **kwargs)

    def get_discount(self, promocode: str) -> int:
        try:
            promo = self._model.objects.get(code=promocode)

            return promo.discount if promo.usages else 0
        except:
            return 0

    def use(self, promocode: str, client_id: int) -> int:
        try:
            promo = self._model.objects.get(code=promocode)

            if not promo.usages:
                raise ValueError
        except:
            return 0

        if not int(promo.usages) <= -1:
            promo.usages = models.F("usages") - 1

        promo.save()

        self._activation_model.objects.create(
            client_id=client_id,
            promocode=promo,
        )

        return promo.discount
