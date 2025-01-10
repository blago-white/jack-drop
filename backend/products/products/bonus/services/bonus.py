from django.db import models

from common.services.base import BaseModelService
from cases.models.cases import Case
from cases.services.cases import CaseService
from items.models.models import Item

from ..models import UserBonusBuyProfile, BonusBuyLevel, BonusCase, UserBonus, BonusTypes


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


class BonusCaseService(BaseModelService):
    default_model = BonusCase

    def create(self, case_id: int,
               discount: int = 0,
               free: str = False) -> BonusCase:
        return self._model.objects.create(
            case_id=case_id,
            discount=discount,
            is_free=free
        )


class UserBonusesService(BaseModelService):
    default_model = UserBonus

    def get_all(self, user_id: int) -> models.QuerySet:
        return self._model.objects.select_related(
            "related_case__case",
            "related_case",
            "related_item",
        ).filter(
            user_id=user_id, active=True
        ).annotate(
            case_title=models.F("related_case__case__title"),
            case_discount=models.F("related_case__discount"),
            case_is_free=models.F("related_case__is_free"),
            item_title=models.F("related_item__title")
        ).values(
            "bonus_type",
            "case_title",
            "case_discount",
            "case_is_free",
            "item_title"
        ).order_by("-date_receive")

    def get_discount(self, user_id: int, case_id: int) -> int:
        try:
            return self._model.objects.select_related("related_case").filter(
                user_id=user_id,
                related_case__case__id=case_id,
                active=True
            ).first().related_case.discount
        except Exception as e:
            return 0

    def get_all_discounts(self, user_id: int) -> int:
        return self._model.objects.filter(
            user_id=user_id, active=True
        ).annotate(
            case=models.F("related_case__case__pk"),
            discount=models.F("related_case__discount")
        ).values(
            "case", "discount"
        ).order_by("discount")

    def add_discount(self, user_id: int, bonus_case: BonusCase):
        return self._model.objects.create(
            related_case=bonus_case,
            user_id=user_id,
            bonus_type=BonusTypes.CASE_DISCOUNT,
        )

    def pop_discount(self, user_id: int, case_id: int) -> int:
        return self._model.objects.filter(
            user_id=user_id,
            related_case__case__id=case_id,
            active=True
        ).first().delete()

    def add_upgrade_item(self, user_id: int, item: Item) -> UserBonus:
        return self._add_item(user_id=user_id,
                              item=item,
                              type_=BonusTypes.FREE_UPGRADE_SKIN)

    def add_contract_item(self, user_id: int, item: Item) -> UserBonus:
        return self._add_item(user_id=user_id,
                              item=item,
                              type_=BonusTypes.FREE_CONTRACT_SKIN)

    def add_free_item(self, user_id: int, item: Item) -> UserBonus:
        return self._add_item(user_id=user_id,
                              item=item,
                              type_=BonusTypes.FREE_SKIN)

    def _add_item(self, user_id: int,
                  item: Item,
                  type_: BonusTypes) -> UserBonus:
        return self._model.objects.create(
            user_id=user_id,
            related_item=item,
            bonus_type=type_
        )


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

        profile.full_clean()
        profile.save()

        return True

    def add_points(self, user_id: int, points: int) -> bool:
        count = self._model.objects.filter(user_id=user_id).update(
            points=models.F("points") + points
        )

        return bool(count)

    def add_case(self, user_id: int, case: Case) -> bool:
        profile: UserBonusBuyProfile = self.get_or_create(user_id=user_id)

        if self.has_withdrawed_case(user_id=user_id, case_id=case.id):
            return True

        profile.free_cases.add(case)

        return True

    def withdraw_case(self, user_id: int) -> Case:
        profile = self.get_or_create(user_id=user_id)

        if profile.points < profile.level.target:
            return False

        case = profile.level.free_case

        if self.has_withdrawed_case(user_id=user_id, case_id=case.pk):
            return False

        profile.free_cases.add(case)

        profile.full_clean()
        profile.save()

        return case

    def has_withdrawed_case(self, user_id: int, case_id: int) -> bool:
        return self.get_or_create(user_id=user_id).free_cases.filter(
            pk=case_id
        ).exists()

    def get_withdrawed_cases(self, user_id: int) -> list[Case]:
        return self.get_or_create(user_id=user_id).free_cases.all()

    def can_withdraw(self, user_id: int) -> bool:
        profile: UserBonusBuyProfile = self.get_or_create(user_id=user_id)
        already_withdrawed = profile.free_cases.filter(
            pk=profile.level.free_case.pk
        )

        return ((profile.points > profile.level.target) and
                not already_withdrawed)

    def use_bonus_case(self, user_id: int, case_id: int) -> bool:
        profile = self.get_or_create(user_id=user_id)

        profile.free_cases.remove(
            self._case_service.get(case_id=case_id)
        )

        return True
