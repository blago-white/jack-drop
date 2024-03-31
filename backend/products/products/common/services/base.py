from abc import ABCMeta, abstractmethod

from django.db import models
from django.core.exceptions import ValidationError
from django.db import models


class BaseModelService(metaclass=ABCMeta):
    def __init__(self, model: models.Model = None):
        self._model = model if model is not None else self._model

    @property
    @abstractmethod
    def _model(self) -> models.Model:
        pass


class AbstractReadOnlyService(BaseModelService, metaclass=ABCMeta):
    @abstractmethod
    def get_all(self) -> models.QuerySet:
        pass

    @abstractmethod
    def get(self, pk) -> models.Model:
        pass


class AbstractModelService(AbstractReadOnlyService, metaclass=ABCMeta):
    @abstractmethod
    def create(self, data) -> models.Model:
        pass

    @abstractmethod
    def update(self, pk, data) -> models.Model:
        pass

    @abstractmethod
    def delete(self, data) -> None:
        pass
