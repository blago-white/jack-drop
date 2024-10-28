from abc import ABCMeta, abstractmethod

from django.db import models

from cases.models.items import CaseItem
from items.models.models import Item


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
    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()

    def get_case_items_for_case(self, case_pk: str) -> models.QuerySet:
        return self._model.objects.filter(
            case=case_pk,
            item__price__gt=0
        ).order_by("rate")

    def get_case_items_for_case_by_price(self, case_pk: str):
        return self._model.objects.filter(
            case=case_pk,
            item__price__gt=0
        ).order_by("item__price")

    def get_drop_case_items_for_case(self, case_pk: str) -> dict:
        return self.get_case_items_for_case(case_pk=case_pk).order_by(
            "rate"
        ).annotate(
            price=models.F("item__price")
        ).annotate(title=models.F("item__title"),
                   image_path=models.F("item__image_path")).values(
            "id", "item_id", "rate", "price", "title", "image_path"
        )

    def bulk_update_rates(
            self, rates: list[float],
            case_items: models.QuerySet[CaseItem]) -> int:
        for values in zip(rates, case_items, strict=True):
            values[1].rate = values[0]

        self._model.objects.bulk_update(case_items, ["rate"])

    def get(self, item_id: int) -> CaseItem:
        return self._model.objects.get(pk=item_id)

    def bulk_get_items(self, item_ids: list[int]) -> models.QuerySet[CaseItem]:
        return self._model.objects.filter(
            pk__in=item_ids
        ).select_related("item").annotate(
            price=models.F("item__price"),
            title=models.F("item__title"),
            image_path=models.F("item__image_path")
        ).values(
            "pk", "price", "title", "image_path"
        )

    @staticmethod
    def get_related_items(
            case_items_queryset: models.QuerySet[CaseItem]
    ) -> models.QuerySet:
        return Item.objects.filter(
            pk__in=case_items_queryset.values_list("item", flat=True)
        ).order_by("price")
