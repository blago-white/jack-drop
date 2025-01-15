from abc import abstractmethod, ABCMeta

from django.db import models

from cases.models.items import CaseItem
from cases.services.cases import CaseService
from items.models.models import Item
from .items import BaseCaseItemsService, CaseItemsService


class BaseCaseItemsChancesService(metaclass=ABCMeta):
    def __init__(self, price_field_name: str = "price"):
        self._price_field_name = price_field_name

    @abstractmethod
    def update_chanses(self, case: models.Model) -> None:
        pass


class CaseItemsChancesService(BaseCaseItemsChancesService):
    _model: models.Model = CaseItem
    _service: BaseCaseItemsService
    _cases_service: CaseService

    def __init__(
            self, *args,
            model: CaseItem = None,
            service: BaseCaseItemsService = None,
            cases_service: CaseService = None,
            **kwargs):
        self._model = model or self._model
        self._service = service or CaseItemsService(model=model)
        self._cases_service = cases_service or CaseService()

        super().__init__(*args, **kwargs)

    def update_chances_for_all(self):
        for case in self._cases_service.get_all():
            self.update_chanses(case=case)

    def update_chanses(self, case: models.Model) -> None:
        case_items = self._service.get_case_items_for_case_by_price(
            case_pk=case.pk
        )
        items = self._service.get_related_items(
            case_items_queryset=case_items
        )

        percentage = self._calculate_chanses(items_of_case=items)

        self._service.bulk_update_rates(rates=percentage,
                                        case_items=case_items)

    def _calculate_chanses(
            self,
            items_of_case: models.QuerySet[Item]
            ) -> list[int]:
        if not items_of_case:
            return []

        pricing: list[float] = items_of_case.values_list(
            self._price_field_name, flat=True
        )

        print(f"CHANCES PRICING: {pricing}")

        percent_value = sum(pricing) / 100

        chances = list(reversed(list(map(
            lambda x: round(x / percent_value, 3),
            pricing
        ))))

        print(f"CHANCES: {chances}")

        return chances
