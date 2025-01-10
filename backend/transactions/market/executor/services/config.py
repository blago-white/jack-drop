from common.services.base import BaseModelService

from executor.models import Config


class ConfigModelService(BaseModelService):
    default_model = Config

    def get_interval(self) -> int:
        result = self._model.objects.all().first()

        if result:
            return result.withdraw_interval_seconds
        else:
            return 5*60

    def get_withdraw_callback_url(self) -> str | None:
        result = self._model.objects.all().first()

        if result:
            return result.withdraw_callback_url
