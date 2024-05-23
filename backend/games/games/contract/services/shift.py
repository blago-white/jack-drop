from common.services.base import BaseModelService

from ..models import ContractShift


class ContractShiftService(BaseModelService):
    default_model = ContractShift

    def get_shift(self) -> int:
        return self._model.objects.filter(active=True).first().shift
