from abc import ABCMeta, abstractmethod

from django.db import models

from market.models import apikey

from  .exceptions import APIKeyNotConfiguredException


class AbstractMarketAPIKeyService(metaclass=ABCMeta):
    _model: models.Model

    def __init__(self, model: models.Model = apikey.ApiKey):
        self._model = model

    @property
    @abstractmethod
    def apikey(self) -> str:
        pass


class MarketAPIKeyService(AbstractMarketAPIKeyService):
    @property
    def apikey(self) -> str:
        api_key: apikey.ApiKey = self._model.objects.filter(
            active=True
        ).first()

        if api_key is None:
            raise APIKeyNotConfiguredException(
                "Add API key"
            )

        return api_key.key
