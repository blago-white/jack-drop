from common.repositories import BaseRepository
from ..serializers import DiscountSerializer
from ..services.discount import PromocodesService


class DiscountRepository(BaseRepository):
    default_service = PromocodesService()
    default_serializer_class = DiscountSerializer

    _service: PromocodesService

    def get(self, promocode: int | str) -> dict:
        serialized = self._serializer_class(
            instance=self._service.get_discount(promocode=promocode)
        )

        return serialized.data
