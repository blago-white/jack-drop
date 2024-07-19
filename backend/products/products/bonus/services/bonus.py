from django.db import models

from common.services.base import BaseModelService

from ..models import UserBonusBuyProfile, BonusBuyLevel


class BonusBuyLevelService(BaseModelService):
    default_model = BonusBuyLevel

    def get_next(self, level: BonusBuyLevel) -> BonusBuyLevel:
        if level.level > self._model.objects.all().order_by(
                "-level"
        ).first():
            return False

        return self._models.objects.filter(
            pk=level.level + 1
        )


class BonusBuyService(BaseModelService):
    default_model = UserBonusBuyProfile
    default_level_service = BonusBuyLevelService()

    def __init__(self, *args,
                 level_service: BonusBuyLevelService = None,
                 **kwargs):
        self._level_service = level_service or self.default_level_service

        super().__init__(*args, **kwargs)

    def get_or_create(self, user_id: int) -> UserBonusBuyProfile:
        if qs := self._model.objects.filter(pk=user_id):
            return qs.first()

        return self.create(user_id=user_id)

    def create(self, user_id: int) -> UserBonusBuyProfile:
        return self._model.objects.create(user_id=user_id)

    def next_level(self, user_id: int) -> bool:
        profile = self.get_or_create(user_id=user_id)

        if profile.points < profile.level.target:
            return False

        profile.level = self._level_service.get_next(level=profile.level)

        if not profile.level:
            return False

        profile.full_clean()
        profile.save()

        return True

    def add_points(self, user_id: int, points: int) -> bool:
        count= self._model.objects.filter(user_id=user_id).update(
            points=models.F("points") + points
        )

        return bool(count)
