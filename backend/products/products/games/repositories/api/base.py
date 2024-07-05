from common.services.base import BaseModelService

from games.api.services.base import BaseApiService


class BaseSimpleApiRepository:
    pass


class BaseApiRepository(BaseSimpleApiRepository):
    default_api_service: BaseApiService
    _api_service: BaseApiService

    def __init__(self, api_service: BaseApiService = None):
        self._api_service = api_service or self.default_api_service


class BaseDualApiRepository(BaseApiRepository):
    default_model_service: BaseModelService
    _model_service: BaseModelService

    def __init__(self, *args,
                 model_service: BaseModelService = None,
                 **kwargs):
        self._model_service = model_service or self.default_model_service

        super().__init__(*args, **kwargs)
