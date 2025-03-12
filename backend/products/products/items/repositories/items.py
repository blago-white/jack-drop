from common.repositories.base import BaseRepository
from ..serializers import ItemSerializer
from ..services.items import ItemService


class ItemsRepository(BaseRepository):
    default_service = ItemService()
    default_serializer_class = ItemSerializer

    _service: ItemService

    def get_all(self, min_price: float = None, max_price: float = None):
        return self._serializer_class(
            instance=self._service.get_all(
                min_price=min_price,
                max_price=max_price
            ),
            many=True
        ).data

    def get(self, item_id: int):
        return self._serializer_class(
            instance=self._service.get(item_id=item_id)
        ).data
