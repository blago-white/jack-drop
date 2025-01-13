from common.services.base import BaseModelService

from cases.models.cases import Case
from ..models import FreeDepositCase, UsedDeposit


class FreeCasesService(BaseModelService):
    default_model = FreeDepositCase

    def get_for_deposit(self, amount: float) -> Case | None:
        return self._model.objects.filter(
            target_deposit_amount__lte=amount
        ).order_by("-target_deposit_amount").first().case


class FreeCasesDepositsService(BaseModelService):
    default_model = UsedDeposit

    def validate_deposit_id(self, deposit_id: int) -> bool:
        return not self._model.objects.filter(pk=deposit_id).exists()

    def use_deposit(self, deposit_id: int):
        return self._model.objects.create(deposit_id=deposit_id)
