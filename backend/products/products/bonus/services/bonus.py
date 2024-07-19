from common.services.base import BaseModelService

from ..models import UserBonusBuyProfile


class BonusBuyService(BaseModelService):
    default_model = UserBonusBuyProfile

    def get_or_create(self, user_id: int) -> UserBonusBuyProfile:
        if qs := self._model.objects.filter(pk=user_id):
            return qs.first()

        return self.create(user_id=user_id)

    def create(self, user_id: int) -> UserBonusBuyProfile:
        return self._model.objects.create(user_id=user_id)

    def next_level(self, user_id: int) -> bool:
        profile = self.get_or_create(user_id=user_id)

        if profile.points < int(profile.get_level_display()):
            return False

        profile.level += 1

        profile.save()
