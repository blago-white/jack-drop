from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository

from ..serialized import LotteryDataSerializer
from ..services.model import LotteryModelService


class LotteryRepository(BaseRepository):
    default_service = LotteryModelService()
    default_serializer_class = LotteryDataSerializer

    _service: LotteryModelService

    def get_current(self):
        lottery = self._service.get_current()

        if not lottery:
            return {"is_active": False}

        return self._serializer_class(
            instance=lottery
        ).data

    def partipicate(self, user_id: int, to_main: bool):
        try:
            self._service.participate(
                participant_id=user_id,
                to_main_lottery=to_main
            )
        except:
            raise ValidationError(detail="Error with adding partipicant!")

        return {"ok": True}
