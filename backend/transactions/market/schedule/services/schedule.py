from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from common.services.base import BaseModelService
from schedule.models import ScheduledItem
from .transfer import ItemInfo


class ScheduleModelService(BaseModelService):
    default_model = ScheduledItem

    def add(self, item: ItemInfo) -> ScheduledItem:
        return self._model.objects.create(
            inventory_item_id=item.inventory_item_id,
            item_market_hash_name=item.item_market_hash_name,
            item_market_link=item.item_market_link,
            price=item.price,
            trade_link=item.trade_link
        )


    def get_schedule(self) -> list[ItemInfo]:
        return list(self._model.objects.all())

    def bulk_delete_withdrawed(self, ids: list[int]):
        print(f"ITEMS: {self._model.objects.all().values()} {ids}")
        self._model.objects.filter(inventory_item_id__in=ids).delete()

    def pop_schedule(self) -> QuerySet:
        result = self.get_schedule()

        self._model.objects.all().delete()

        return result
