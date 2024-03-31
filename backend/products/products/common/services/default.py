from abc import ABCMeta

from django.db import models

from .base import AbstractReadOnlyService


class DefaultModelService(AbstractReadOnlyService, metaclass=ABCMeta):
    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()

    def get(self, pk) -> models.Model:
        return self._model.objects.get(pk=pk)
