from django.db import models

from common.services.base import BaseReadOnlyService
from ..models.models import Item


class ItemService(BaseReadOnlyService):
    default_model = Item

    def get_price(self, item_id: int) -> float:
        return self._model.objects.get(pk=item_id).price

    def set_price(self, item_id: int, item_price: float) -> bool:
        return self._model.objects.filter(pk=item_id).update(
            price=item_price
        ) == 1

    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()

    def get_closest_by_price(self, price: float) -> Item:
        return self._model.objects.filter(
            price__lte=price
        ).order_by("-price").first()
