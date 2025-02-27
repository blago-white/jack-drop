from common.repositories import BaseRepository

from ..serializers import PersonalOfferSerializer
from ..services.offers import PersonalOffersService
from ..services.discount import PromocodesService


class PersonalOffersRepository(BaseRepository):
    default_service = PersonalOffersService()
    default_promocodes_service = PromocodesService()
    default_serializer_class = PersonalOfferSerializer

    _service: PersonalOffersService
    _serializer_class: PersonalOfferSerializer

    def __init__(self, *args,
                 promocodes_service: PromocodesService = None,
                 **kwargs):
        self._promocodes_service = promocodes_service or self.default_promocodes_service

        super().__init__(*args, **kwargs)

    def get(self, client_id: int) -> dict:
        if self._service.can_receive(client_id=client_id):
            return self._serializer_class(
                instance=dict(
                    available=True,
                    promocode=self._promocodes_service.get_for_personal_offer()
                )
            )

        return self._serializer_class().data
