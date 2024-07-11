from django.core.exceptions import ValidationError

from common.services.base import BaseModelService
from ..models import ApiKey


class ApiKeyService(BaseModelService):
    default_model = ApiKey

    @property
    def apikey(self) -> str:
        api_key: ApiKey = self._model.objects.filter(
            active=True
        ).first()

        if api_key is None:
            raise ValidationError(
                "Add API key"
            )

        return api_key.key
