from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.transaction import savepoint_rollback, savepoint

from common.services.base import BaseModelService
from ..models import InventoryItem, Lockings


class InventoryService(BaseModelService):
    default_model = InventoryItem

    def get_all(self, user_id: int = None,
                locked_for: Lockings = None) -> models.QuerySet:

        result = self._model.objects.all().filter(frozen=False)

        if user_id:
            result = result.filter(user_id=user_id)
        if locked_for:
            return result.filter(locked_for=locked_for)

        return result

    def check_ownership(self, owner_id: int,
                        item_id: int = None,
                        inventory_item_id: int = None) -> bool:
        qs = self._model.objects.filter(
            user_id=owner_id,
            frozen=False
        )

        if item_id:
            qs = qs.filter(item_id=item_id)
        elif inventory_item_id:
            qs = qs.filter(pk=inventory_item_id)

        return qs.exists()

    def bulk_remove_from_inventory(self, inventory_items_ids: list[int],
                                   owner_id: int = None) -> bool:
        sid = savepoint()

        qs = self._model.objects.filter(
            pk__in=inventory_items_ids
        )

        if owner_id:
            qs = qs.filter(user_id=owner_id)

        deleted, _ = qs.delete()

        if len(inventory_items_ids) != deleted:
            savepoint_rollback(sid)
            return False

        return True

    def remove_from_inventory(self, owner_id: int,
                              item_id: int = None,
                              inventory_item_id: int = None) -> bool:
        if item_id:
            return self._model.objects.filter(
                pk__in=self._model.objects.filter(
                    user_id=owner_id,
                    item_id=item_id
                ).values_list("pk", flat=True)[:1],
            ).delete()[0]

        return self._model.objects.filter(
            user_id=owner_id, pk=inventory_item_id
        ).delete()[0]

    def freeze_inventory_item(self, owner_id: int, item_id: int) -> bool:
        item: InventoryItem = self._model.objects.get(
            user_id=owner_id,
            id=item_id
        )

        item.frozen = True

        item.save()

        return True

    def add_item(self, owner_id: int,
                 item_id: int,
                 locking: str = Lockings.UNLOCK) -> InventoryItem:
        return self._model.objects.create(
            user_id=owner_id,
            item_id=item_id,
            locked_for=locking
        )

    def bulk_add_item(self, items_ids: list[int], owner_id: int) -> list[InventoryItem]:
        created = self._model.objects.bulk_create(
            [self._model(
                user_id=owner_id,
                item_id=item_id
            ) for item_id in items_ids]
        )

        return created

    def bulk_get_items_amount(
            self, owner_id: int,
            inventory_items_ids: list[int]) -> float:
        items = self._model.objects.filter(
            user_id=owner_id,
            id__in=inventory_items_ids,
            frozen=False
        )

        if items.count() < len(inventory_items_ids):
            raise ObjectDoesNotExist(
                "Some items were not found in the inventory"
            )

        return items.aggregate(prices_sum=models.Sum("item__price")).get(
            "prices_sum"
        )

    def get_item(self, inventory_item_id: int, apply_frozen: bool = False) -> InventoryItem:
        print("GET INV ITEM", inventory_item_id, self._model.objects.all().order_by("-pk").values("pk"))

        result = self._model.objects.filter(
            models.Q(frozen=False) | models.Q(frozen=apply_frozen),
            pk=inventory_item_id,
        ).first()

        print(result)

        return result

    def bulk_unfreeze(self, items_ids: list[int]):
        return bool(self._model.objects.filter(id__in=items_ids).update(
            frozen=False
        ))
