from common.services.base import BaseModelService

from ..models import Config


class ConfigService(BaseModelService):
    default_model = Config

    def get(self) -> Config:
        return self._model.objects.all().first()
