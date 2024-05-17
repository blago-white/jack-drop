from abc import ABCMeta, abstractmethod

from django.db import models


class BaseReadOnlyService(metaclass=ABCMeta):
    _model: models.Model
    default_model: models.Model | None

    def __init__(self, model: models.Model = None):
        if model is None:
            try:
                self._model = self.default_model
            except AttributeError:
                raise AttributeError(
                    "Model was not specifiend, fill the `default_model` field"
                )

        else:
            self._model = model

    @abstractmethod
    def get(self, *args, **kwargs) -> models.QuerySet:
        pass
