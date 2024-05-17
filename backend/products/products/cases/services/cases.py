import typing
from abc import ABCMeta, abstractmethod

from django.db import models

from items.models.models import Item
from ..models.cases import Case
from common.services.base import BaseReadOnlyService

if typing.TYPE_CHECKING:
    from cases.models.items import CaseItem
else:
    CaseItem = models.Model


class BaseCaseItemsService(metaclass=ABCMeta):
    _model: CaseItem

    def __init__(self, model: CaseItem):
        self._model = model

    @abstractmethod
    def get_case_items_for_case(self, case):
        pass

    @abstractmethod
    def bulk_update_chances(self, chances, case_items):
        pass

    @staticmethod
    @abstractmethod
    def get_related_items(case_items_queryset):
        pass


class CaseItemsService(BaseCaseItemsService):
    def get_case_items_for_case(self, case: models.Model):
        return self._model.objects.filter(case=case)

    def bulk_update_chances(self, chances: list[float],
                            case_items: models.QuerySet[CaseItem]) -> int:
        for values in zip(chances, case_items, strict=True):
            values[1].chance = values[0]

        self._model.objects.bulk_update(case_items, ["chance"])

    @staticmethod
    def get_related_items(
            case_items_queryset: models.QuerySet[CaseItem]
    ) -> models.QuerySet:
        return Item.objects.filter(
            pk__in=case_items_queryset.values_list("item", flat=True)
        )


class CaseService(BaseReadOnlyService):
    default_model = Case

    def get(self, case_id: int) -> models.Model:
        return self._model.objects.get(pk=case_id)
