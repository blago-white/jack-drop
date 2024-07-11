from common.repositories.base import BaseRepository

from ..services.items import ItemService
from ..serializers import ItemSerializer


class ItemsRepository(BaseRepository):
    default_service = ItemService()
    default_serializer_class = ItemSerializer

    def get_all(self, min_price: float = None, max_price: float = None):
        return self._serializer_class(
            instance=self._service.get_all(
                min_price=min_price,
                max_price=max_price
            ),
            many=True
        ).data
