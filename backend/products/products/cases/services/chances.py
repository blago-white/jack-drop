from abc import abstractmethod, ABCMeta

from django.db import models

from cases.models.items import CaseItem
from items.models.models import Item
from .cases import BaseCaseItemsService, CaseItemsService


class BaseCaseItemsChancesService(metaclass=ABCMeta):
    def __init__(self, price_field_name: str = "price"):
        self._price_field_name = price_field_name

    @abstractmethod
    def update_chanses(self, case: models.Model) -> None:
        pass


class CaseItemsChancesService(BaseCaseItemsChancesService):
    _model: models.Model = CaseItem
    _service: BaseCaseItemsService

    def __init__(self, *args,
                 model: CaseItem = None,
                 service: BaseCaseItemsService = None,
                 **kwargs):
        self._model = model or self._model
        self._service = service or CaseItemsService(model=model)

        super().__init__(*args, **kwargs)

    def update_chanses(self, case: models.Model) -> None:
        case_items = self._service.get_case_items_for_case(case=case)
        items = self._service.get_related_items(
            case_items_queryset=case_items
        )

        percentage = self._calculate_chanses(items_of_case=items)

        self._service.bulk_update_chances(chances=percentage,
                                          case_items=case_items)

    def _calculate_chanses(self,
                           items_of_case: models.QuerySet[Item]
                           ) -> list[int]:
        pricing: list[float] = items_of_case.values_list(
            self._price_field_name, flat=True
        )

        percent_value = 100 / sum(pricing)

        return reversed(list(map(
            lambda x: round(x * percent_value / 100, 3),
            pricing
        )))
