from common.repositories.base import BaseRepository
from ..serializers import ItemPriceSerializer
from ..services.items import ItemService


class ItemPriceRepository(BaseRepository):
    default_service = ItemService()
    default_serializer_class = ItemPriceSerializer

    def get_price(self, item_id: int) -> dict:
        return self._serializer_class(
            instance=dict(
                item_id=item_id,
                price=self._service.get_price(item_id=item_id)
            )
        ).data
