from django.db import models

from common.services.base import BaseReadOnlyService
from ..models.cases import Case


class CaseService(BaseReadOnlyService):
    default_model = Case

    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()

    def get(self, case_id: int) -> Case:
        return self._model.objects.get(pk=case_id)

    def get_price(self, case_id: int) -> int | float:
        return self.get(case_id=case_id).price
