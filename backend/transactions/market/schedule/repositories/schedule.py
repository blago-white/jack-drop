from rest_framework.exceptions import ValidationError
from common.repositories.base import BaseRepository

from schedule.serializers import WithdrawItemSerializer
from schedule.services.schedule import ScheduleModelService
from schedule.services.banned import BannedOwnersModelService
from schedule.services.transfer import ItemInfo


class ScheduleRepository(BaseRepository):
    default_serializer_class = WithdrawItemSerializer
    default_service = ScheduleModelService()
    default_banned_service = BannedOwnersModelService()
    default_dataclass = ItemInfo

    def __init__(self, *args,
                 dataclass: ItemInfo = None,
                 banned_service: BannedOwnersModelService = None,
                 **kwargs):
        self._dataclass = dataclass or self.default_dataclass
        self._banned_service = banned_service or self.default_banned_service

        super().__init__(*args, **kwargs)

    def add(self, request_data: dict) -> dict:
        serialized: WithdrawItemSerializer = self._serializer_class(
            data=request_data
        )

        serialized.is_valid(raise_exception=True)

        if self._banned_service.is_banned(
                owner_id=serialized.data.get("owner_id")
        ):
            raise ValidationError("Cannot withdraw, your banned!")

        result = self._service.add(item=self._serializer_to_dataclass(
            serialized=serialized
        ))

        if not result:
            raise ValidationError("Cannot add this item", code=400)

        return {"ok": True}

    def _serializer_to_dataclass(self, serialized: WithdrawItemSerializer):
        data = serialized.data

        return self._dataclass(
            item_market_hash_name=data.get("inventory_item_hash_name"),
            price=data.get("item_price"),
            item_market_link=data.get("item_market_link"),
            trade_link=data.get("owner_trade_link"),
            inventory_item_id=data.get("inventory_item_id"),
        )
