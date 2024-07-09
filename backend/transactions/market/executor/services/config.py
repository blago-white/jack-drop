from common.services.base import BaseModelService

from executor.models import Config


class ConfigModelService(BaseModelService):
    default_model = Config

    def get_interval(self) -> int:
        return self._model.objects.all().first().withdraw_interval_seconds
