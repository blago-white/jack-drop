from common.services.base import BaseService

from ..models import FreezeFundsPercent


class FreezeFundsService(BaseService):
    default_model = FreezeFundsPercent

    def get(self):
        try:
            return self._model.objects.first().percent
        except Exception as e:
            return 0
