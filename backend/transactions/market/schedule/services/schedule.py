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
            price=item.price,
            trade_link=item.trade_link
        )

    def pop_schedule(self) -> QuerySet:
        result = self._model.objects.all()

        result_ok = result.delete()[0]

        if not result_ok:
            raise ValidationError("Empty sequence")

        return result
