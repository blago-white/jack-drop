from common.services.base import BaseModelService

from ..models.fortune import FortuneWheelBan


class FortuneWheelService(BaseModelService):
    default_model = FortuneWheelBan

    def can_play(self, user_id: int):
        try:
            return self._model.objects.get(user_id=user_id) is None
        except:
            return True

    def make_play(self, user_id: int):
        print("MAKE PLAY")

        result = bool(self.can_play(user_id=user_id))

        if result:
            self._model.objects.create(user_id=user_id)

        return result

    def drop_ban(self, user_id: int):
        self._model.objects.filter(user_id=user_id).delete()
