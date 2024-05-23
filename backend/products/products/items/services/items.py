from django.db import models

from common.services.base import BaseReadOnlyService
from ..models.models import Item


class ItemService(BaseReadOnlyService):
    default_model = Item

    def get_price(self, item_id: int) -> float:
        return self._model.objects.get_user_info(pk=item_id).price

    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()

    def get_closest_by_price(self, price: float) -> Item:
        return self._model.objects.filter(
            price__lte=price
        ).order_by("-price").first()
