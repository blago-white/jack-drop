from common.services.base import BaseModelService

from ..models import Config


class ConfigService(BaseModelService):
    default_model = Config

    def get(self) -> Config:
        return Config(
            apikey = "S",
            api_user_id = "S",
            bank_address = "S"
        )

        return self._model.objects.all().first()
