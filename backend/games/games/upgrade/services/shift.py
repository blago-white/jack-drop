from common.services.base import BaseModelService

from ..models import ChanceShift


class ChanceShiftService(BaseModelService):
    default_model = ChanceShift

    def get(self) -> int:
        return self._model.objects.filter(active=True).first().shift
