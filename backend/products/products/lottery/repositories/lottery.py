from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository

from ..serialized import LotteryDataSerializer
from ..services.model import LotteryModelService


class LotteryRepository(BaseRepository):
    default_service = LotteryModelService()
    default_serializer_class = LotteryDataSerializer

    _service: LotteryModelService

    def get_current(self, user_id: int = None):
        lottery = self._service.get_current()

        if not lottery:
            return {"is_active": False}

        if user_id:
            takes_part_in = self._service.has_participate(
                participant_id=user_id
            )
        else:
            takes_part_in = False, False

        return self._serializer_class(
            instance=lottery
        ).data | {
            "take_part_main": takes_part_in[0],
            "take_part_second": takes_part_in[1]
        }

    def partipicate(self, user_id: int, to_main: bool):
        try:
            self._service.participate(
                participant_id=user_id,
                to_main_lottery=to_main
            )
        except:
            raise ValidationError(detail="Error with adding partipicant!")

        return {"ok": True}
