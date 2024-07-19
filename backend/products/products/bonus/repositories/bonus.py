from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository

from ..services.bonus import BonusBuyService
from ..serializers import BonusBuyProfileSerializer


class BonusBuyRepository(BaseRepository):
    default_service = BonusBuyService()
    default_serializer_class = BonusBuyProfileSerializer

    _service: BonusBuyService

    def get(self, user_id: int) -> dict:
        return self._serializer_class(
            instance=self._service.get_or_create(user_id=user_id)
        ).data

    def next_level(self, user_id: int) -> dict:
        result = self._service.next_level(user_id=user_id)

        if not result:
            raise ValidationError("Not enought points!")

        return {"ok": result}
