from django.db import models

from common.services.base import BaseModelService
from cases.models.cases import Case
from cases.services.cases import CaseService

from ..models import UserBonusBuyProfile, BonusBuyLevel, CaseDiscount


class BonusBuyLevelService(BaseModelService):
    default_model = BonusBuyLevel

    def get_next(self, level: BonusBuyLevel) -> BonusBuyLevel:
        if level.level > self._model.objects.all().order_by(
                "-level"
        ).first().level:
            return False

        return self._model.objects.filter(
            pk=level.level + 1
        ).first()

    def get_prev(self, level: BonusBuyLevel) -> BonusBuyLevel:
        if level.level < 1:
            return False

        return self._model.objects.filter(
            pk=max(level.level - 1, 1)
        ).first()


class BonusBuyService(BaseModelService):
    default_model = UserBonusBuyProfile
    default_level_service = BonusBuyLevelService()
    default_case_service = CaseService()

    def __init__(self, *args,
                 level_service: BonusBuyLevelService = None,
                 case_service: CaseService = None,
                 **kwargs):
        self._level_service = level_service or self.default_level_service
        self._case_service = case_service or self.default_case_service

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

        profile.withdraw_current = False

        profile.full_clean()
        profile.save()

        return True

    def add_points(self, user_id: int, points: int) -> bool:
        count = self._model.objects.filter(user_id=user_id).update(
            points=models.F("points") + points
        )

        return bool(count)

    def add_case(self, user_id: int, case: Case) -> bool:
        profile = self.get_or_create(user_id=user_id)

        profile.active_free_cases.add(case)

        return True

    def withdraw_case(self, user_id: int) -> Case:
        profile = self.get_or_create(user_id=user_id)

        if profile.points < profile.level.target:
            return False

        case = profile.level.free_case

        if profile.active_free_cases.filter(id=case.id):
            return False

        profile.withdraw_current = True
        profile.active_free_cases.add(case)

        profile.full_clean()
        profile.save()

        return case

    def has_withdrawed_case(self, user_id: int, case_id: int) -> bool:
        return self.get_or_create(user_id=user_id).active_free_cases.filter(
            id=case_id
        ).exists()

    def can_withdraw(self, user_id: int) -> bool:
        profile: UserBonusBuyProfile = self.get_or_create(user_id=user_id)

        if (not profile.withdraw_current and
                profile.points > profile.level.target):
            return True

        else:
            return False

    def user_bonus_case(self, user_id: int, case_id: int) -> bool:
        profile = self.get_or_create(user_id=user_id)

        profile.active_free_cases.remove(
            self._case_service.get(case_id=case_id)
        )

        return True

    def get_discount(self, user_id: int, case_id: int) -> int:
        try:
            return self._model.objects.get(
                user_id=user_id,
            ).cases_discounts.filter(case_id=case_id).first().discount
        except:
            return 0

    def add_discount(self, user_id: int, case_id: int, discount: int):
        self._model.objects.get(
                user_id=user_id,
            ).cases_discounts.add(
                CaseDiscount.objects.create(
                    case_id=case_id,
                    user_id=user_id,
                    discount=discount
            )
        )

    def pop_discount(self, user_id: int, case_id: int) -> int:
        return self._model.objects.get(
                user_id=user_id,
            ).cases_discounts.filter(case_id=case_id).first().delete()
