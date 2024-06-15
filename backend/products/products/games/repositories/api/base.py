from common.services.base import BaseReadOnlyService

from games.api.services.base import BaseApiService


class BaseSimpleApiRepository:
    pass


class BaseApiRepository(BaseSimpleApiRepository):
    default_api_service: BaseApiService
    _api_service: BaseApiService

    def __init__(self, api_service: BaseApiService = None):
        self._api_service = api_service or self.default_api_service


class BaseDualApiRepository(BaseApiRepository):
    default_model_service: BaseReadOnlyService
    _model_service: BaseReadOnlyService

    def __init__(self, *args,
                 model_service: BaseReadOnlyService = None,
                 **kwargs):
        self._model_service = model_service or self.default_model_service

        super().__init__(*args, **kwargs)
