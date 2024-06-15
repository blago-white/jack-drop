from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from common.services.base import BaseReadOnlyService
from ..models import InventoryItem


class InventoryService(BaseReadOnlyService):
    default_model = InventoryItem

    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()

    def check_ownership(self, owner_id: int, item_id: int) -> bool:
        return self._model.objects.filter(
            user_id=owner_id,
            item_id=item_id
        ).exists()

    def remove_from_inventory(self, owner_id: int, item_id: int) -> bool:
        return self._model.objects.filter(
            owner_id=owner_id,
            item_id=item_id
        )[:1].delete() > 0

    def add_item(self, owner_id: int, item_id: int) -> InventoryItem:
        return self._model.objects.create(
            user_id=owner_id,
            item_id=item_id
        )

    def bulk_get_items_amount(self, owner_id: int,
                              inventory_items_ids: list[int]) -> float:
        items = self._model.objects.filter(
            user_id=owner_id,
            id__in=inventory_items_ids
        ).distinct("item_id")

        if items.count() < len(inventory_items_ids):
            raise ObjectDoesNotExist(
                "Some items were not found in the inventory"
            )

        return items.aggregate(prices_sum=models.Sum("item__price")).get(
            "prices_sum"
        )
