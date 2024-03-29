from abc import ABCMeta, abstractmethod

from django.db import models
from django.core.exceptions import ValidationError
from django.db import models


class BaseReadOnlyService(metaclass=ABCMeta):
    @abstractmethod
    def get(self, *args, **kwargs) -> models.QuerySet:
        pass


class AbstractModelService(metaclass=ABCMeta):
    def __init__(self, model: models.Model = None):
        self._model = model if model is not None else self._model

    @property
    @abstractmethod
    def _model(self) -> models.Model:
        pass

    @abstractmethod
    def get_all(self) -> models.QuerySet:
        pass

    @abstractmethod
    def get(self, pk) -> models.Model:
        pass

    @abstractmethod
    def create(self, data) -> models.Model:
        pass

    @abstractmethod
    def update(self, pk, data) -> models.Model:
        pass

    @abstractmethod
    def delete(self, data) -> None:
        pass


class BaseModelService(AbstractModelService, metaclass=ABCMeta):
    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()

    def get(self, pk) -> models.Model:
        return self._model.objects.get(pk=pk)

    def create(self, data) -> models.Model:
        instance: models.Model = self._model.objects.create(**data)

        return instance.save()

    def update(self, pk, data) -> models.Model:
        try:
            instance, created = self._model.objects.update_or_create(
                pk=pk,
                defaults=dict(**data)
            )
        except ValidationError:
            raise ValidationError("Object does not exists or data for update is not correct")

        return instance.save()

    def delete(self, pk) -> None:
        self.get(pk=pk).delete()
