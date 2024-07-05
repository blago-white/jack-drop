from django.db import models

from common.services.base import BaseModelService
from ..models.cases import Case


class CaseService(BaseModelService):
    default_model = Case

    def get_paid(self) -> models.QuerySet:
        return self.get_all().filter(price__gt=0)

    def get_all(self) -> models.QuerySet:
        return self._model.objects.all().alias(count_items=models.Count(
            "items"
        )).filter(count_items__gt=0)

    def bulk_get(self, case_ids: list[int]) -> models.QuerySet[Case]:
        return self._model.objects.filter(pk__in=case_ids)

    def get(self, case_id: int) -> Case:
        return self._model.objects.get(pk=case_id)

    def get_price(self, case_id: int) -> int | float:
        return self.get(case_id=case_id).price

    def get_all_for_category(self, category: str,
                             min_price: int = None,
                             max_price: int = None) -> models.QuerySet:
        result = self._model.objects.filter(category__title=category)

        if min_price is not None:
            result = result.filter(price__gte=min_price)

        if max_price is not None:
            result = result.filter(price__lte=max_price)

        return result
