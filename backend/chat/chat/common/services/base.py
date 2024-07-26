from django.db import models


class BaseModelService:
    default_model: models.Model

    def __init__(self, model: models.Model = None):
        self._model = model or self.default_model
