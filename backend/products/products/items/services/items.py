import random

from django.db import models

from common.services.base import BaseModelService
from ..models.models import Item


class ItemService(BaseModelService):
    default_model = Item

    def get_price(self, item_id: int) -> float:
        return self._model.objects.get(pk=item_id).price

    def get(self, item_id: int) -> Item:
        return self._model.objects.get(pk=item_id)

    def bulk_get_price(self, items_ids: list[int]) -> float:
        return self._model.objects.filter(pk__in=items_ids).aggregate(
            total=models.Sum("price")
        ).get("total")

    def set_price(self, item_id: int, item_price: float) -> bool:
        return self._model.objects.filter(pk=item_id).update(
            price=item_price
        ) == 1

    def bulk_set_price(self, items: list[Item]):
        return self._model.objects.bulk_update(items, ["price"])

    def get_all(self, min_price: float = None,
                max_price: float = None) -> models.QuerySet:
        result = self._model.objects.all().order_by("price").filter(
            price__gte=1
        )

        if min_price:
            result = result.filter(price__gte=min_price)

        if max_price:
            result = result.filter(price__lte=max_price)

        return result

    def get_closest_by_price(self, price: float) -> Item:
        closest = self._model.objects.filter(
            price__lte=price
        ).order_by("-price").first()

        if not closest:
            closest = self._model.objects.filter(
                price__gte=price
            ).order_by("price").first()

        return closest
