from common.repositories.base import BaseRepository

from ..services.fortune import FortuneWheelService


class FortuneWheelModelRepository(BaseRepository):
    default_service = FortuneWheelService()

    _service: FortuneWheelService

    def drop_ban(self, user_id: int):
        try:
            self._service.drop_ban(user_id=user_id)
        except Exception as e:
            return {"ok": False, "detail": e}

        return {"ok": True}
