from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.transaction import savepoint_rollback, savepoint

from common.services.base import BaseModelService
from ..models import InventoryItem, Lockings


class InventoryService(BaseModelService):
    default_model = InventoryItem

    def get_all(self, user_id: int = None,
                locked_for: Lockings = None) -> models.QuerySet:

        result = self._model.objects.all()

        if user_id:
            result = result.filter(user_id=user_id)
        if locked_for:
            return result.filter(locked_for=locked_for)

        return result

    def check_ownership(self, owner_id: int, item_id: int) -> bool:
        return self._model.objects.filter(
            user_id=owner_id,
            item_id=item_id
        ).exists()

    def bulk_remove_from_inventory(self, owner_id: int,
                                   inventory_items_ids: list[int]) -> bool:
        sid = savepoint()

        deleted, _ = self._model.objects.filter(
            pk__in=inventory_items_ids,
            user_id=owner_id
        ).delete()

        if len(inventory_items_ids) != deleted:
            savepoint_rollback(sid)
            return False

        return True

    def remove_from_inventory(self, owner_id: int, item_id: int) -> bool:
        return self._model.objects.filter(
            pk__in=self._model.objects.filter(
                user_id=owner_id,
                item_id=item_id
            ).values_list("pk", flat=True)[:1]
        ).delete()

    def add_item(self, owner_id: int,
                 item_id: int,
                 locking: str = Lockings.UNLOCK) -> InventoryItem:
        return self._model.objects.create(
            user_id=owner_id,
            item_id=item_id,
            locked_for=locking
        )

    def bulk_get_items_amount(
            self, owner_id: int,
            inventory_items_ids: list[int]) -> float:
        items = self._model.objects.filter(
            user_id=owner_id,
            id__in=inventory_items_ids
        )

        if items.count() < len(inventory_items_ids):
            raise ObjectDoesNotExist(
                "Some items were not found in the inventory"
            )

        return items.aggregate(prices_sum=models.Sum("item__price")).get(
            "prices_sum"
        )

    def get_item(self, inventory_item_id: int) -> InventoryItem:
        return self._model.objects.filter(pk=inventory_item_id).first()
