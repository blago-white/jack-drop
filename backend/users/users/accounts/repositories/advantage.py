from common.repositories import BaseRepository
from ..serializers import UpdateAdvantageSerializer
from ..services.advantage import AdvantageService


class AdvantageRepository(BaseRepository):
    default_service = AdvantageService
    default_serializer_class = UpdateAdvantageSerializer

    def update(self, user_id: int, delta_amount: float):
        return {
            "ok": self._service.update(user_id=user_id,
                                       delta_amount=delta_amount)
        }
