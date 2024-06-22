from abc import ABCMeta, abstractmethod

from django.db import models

from items.models.models import Item

from cases.models.items import CaseItem


class BaseCaseItemsService(metaclass=ABCMeta):
    _model: CaseItem = CaseItem

    def __init__(self, model: CaseItem = None):
        self._model = model or self._model

    @abstractmethod
    def get_case_items_for_case(self, case_pk):
        pass

    @abstractmethod
    def bulk_update_rates(self, rates, case_items):
        pass

    @staticmethod
    @abstractmethod
    def get_related_items(case_items_queryset):
        pass


class CaseItemsService(BaseCaseItemsService):
    def get_case_items_for_case(self, case_pk: str) -> models.QuerySet:
        return self._model.objects.filter(case=case_pk)

    def get_drop_case_items_for_case(self, case_pk: str) -> dict:
        return self.get_case_items_for_case(case_pk=case_pk).annotate(
            price=models.F("item__price")
        ).values(
            "id", "rate", "price"
        )

    def bulk_update_rates(
            self, rates: list[float],
            case_items: models.QuerySet[CaseItem]) -> int:
        for values in zip(rates, case_items, strict=True):
            values[1].rate = values[0]

        self._model.objects.bulk_update(case_items, ["rate"])

    @staticmethod
    def get_related_items(
            case_items_queryset: models.QuerySet[CaseItem]
    ) -> models.QuerySet:
        return Item.objects.filter(
            pk__in=case_items_queryset.values_list("item", flat=True)
        )
