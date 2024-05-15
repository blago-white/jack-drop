from common.repositories import BaseRepository
from ..serializers import DiscountSerializer
from ..services.discount import DiscountService


class DiscountRepository(BaseRepository):
    default_service = DiscountService()
    default_serializer_class = DiscountSerializer

    def get(self, pk: int | str) -> dict:
        serialized = self._serializer_class(
            instance=self._service.get(pk)
        )

        return serialized.data
