from common.services.base import BaseModelService

from cases.models.cases import Case
from ..models import FreeCase, UsedDeposit


class FreeCasesService(BaseModelService):
    default_model = FreeCase

    def get_for_deposit(self, amount: float) -> Case | None:
        return self._model.objects.filter(
            target_deposit_amount__lte=amount
        ).order_by("-target_deposit_amount").first().case


class FreeCasesDepositsService(BaseModelService):
    default_model = UsedDeposit

    def validate_deposit_id(self, deposit_id: int) -> bool:
        return not self._model.objects.filter(pk=deposit_id).exists()
