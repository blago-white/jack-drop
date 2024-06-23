from common.repositories.base import BaseRepository

from ..services.inventory import InventoryService
from ..serializers import InventoryItemSerializer


class InventoryRepository(BaseRepository):
    default_service = InventoryService()
    default_serializer_class = InventoryItemSerializer

    _service: InventoryService

    def get_all(self, user_id: int) -> dict:
        return self._serializer_class(
            instance=self._service.get_all(user_id=user_id),
            many=True
        ).data
