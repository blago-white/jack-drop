from django.db import models


class BaseService:
    default_model: models.Model
    _model: models.Model

    def __init__(self, model: models.Model = None):
        self._model = model or self.default_model