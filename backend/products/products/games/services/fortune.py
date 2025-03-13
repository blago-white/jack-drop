from common.services.base import BaseModelService

from ..models.fortune import FortuneWheelBan


class FortuneWheelService(BaseModelService):
    default_model = FortuneWheelBan

    def can_play(self, user_id: int):
        result = not self._model.objects.filter(user_id=user_id).exists()

        if result:
            self._model.objects.create(user_id=user_id)

        return result

    def drop_ban(self, user_id: int):
        self._model.objects.filter(user_id=user_id).delete()
