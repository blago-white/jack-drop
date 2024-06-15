from abc import ABCMeta

from django.db import models
from django.core.exceptions import ValidationError
from django.db import models


class BaseModelService(metaclass=ABCMeta):
    def __init__(self, model: models.Model = None):
        self._model = model if model is not None else self._model


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
