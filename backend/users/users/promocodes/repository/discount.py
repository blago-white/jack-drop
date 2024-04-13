from common.repositories import BaseRepository

from ..services.discount import DiscountService
from ..serializers import DiscountSerializer


class DiscountRepository(BaseRepository):
    default_service = DiscountService()
    default_serializer_class = DiscountSerializer

    def get(self, pk: int | str) -> dict:
        serialized = self._serializer_class(
            instance=self._service.get(pk)
        )

        return serialized.data
