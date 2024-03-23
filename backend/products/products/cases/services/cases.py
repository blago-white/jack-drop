import typing
from abc import abstractmethod, ABCMeta

from django.db import models

from items.models.models import Item

if typing.TYPE_CHECKING:
    from cases.models.items import CaseItem
else:
    CaseItem = models.Model


class BaseCaseItemsChancesManager(metaclass=ABCMeta):
    def __init__(self, price_field_name: str = "price"):
        self._price_field_name = price_field_name

    @abstractmethod
    def update_chanses(self, case: models.Model) -> None:
        pass


class CaseItemsChancesManager(BaseCaseItemsChancesManager):
    def __init__(self, *args,
                 model: CaseItem,
                 **kwargs):
        self._model = model

        super().__init__(*args, **kwargs)

    def update_chanses(self, case: models.Model) -> None:
        case_items = self._get_related_case_items(case=case)
        items = self._get_related_items(case_items_queryset=case_items)

        percentage = self._calculate_chanses(items_of_case=items)

        for values in zip(percentage, case_items, strict=True):
            values[1].chance = values[0]
            values[1].save()

    def _get_related_case_items(self, case: models.Model) -> models.QuerySet:
        return self._model.objects.filter(case=case)

    @staticmethod
    def _get_related_items(
            case_items_queryset: models.QuerySet
            ) -> models.QuerySet:
        return Item.objects.filter(
            pk__in=case_items_queryset.values_list("item", flat=True)
        )

    def _calculate_chanses(self,
                           items_of_case: models.QuerySet[Item]) -> list[int]:
        pricing: list[float] = items_of_case.values_list(
            self._price_field_name, flat=True
        )

        summary = sum(pricing)

        percent_value = 100 / summary

        return reversed(list(map(
            lambda x: round(x * percent_value / 100, 3),
            pricing
        )))
