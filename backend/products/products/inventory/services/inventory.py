from common.services.base import BaseReadOnlyService

from ..models import InventoryItem


class InventoryService(BaseReadOnlyService):
    default_model = InventoryItem

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
