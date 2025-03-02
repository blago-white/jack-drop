from common.repositories import BaseRepository
from ..serializers import DiscountSerializer
from ..services.discount import PromocodesService


class DiscountRepository(BaseRepository):
    default_service = PromocodesService()
    default_serializer_class = DiscountSerializer

    _service: PromocodesService

    def get(self, promocode: int | str) -> dict:
        return {
            "discount": self._service.get_discount(promocode=promocode)
        }
