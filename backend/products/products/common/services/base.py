from abc import ABCMeta, abstractmethod

from django.db import models


class BaseReadOnlyService(metaclass=ABCMeta):
    @abstractmethod
    def get(self, *args, **kwargs) -> models.QuerySet:
        pass
