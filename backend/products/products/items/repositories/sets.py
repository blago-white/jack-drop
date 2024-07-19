from common.repositories.base import BaseRepository

from ..services.sets import ItemSetService
from ..serializers import ItemsSetSerializer


class ItemsSetsRepository(BaseRepository):
    default_service = ItemSetService()
    default_serializer_class = ItemsSetSerializer

    def get_all(self) -> dict:
        return self._serializer_class(
            instance=self._service.get_all(),
            many=True
        ).data
