from abc import ABCMeta, abstractmethod
from rest_framework import serializers

from common.services import base

from ..services.base import BaseModelService


RequestPostData = dict[str, int | str]
PrimaryKey = int


class BaseCRUDRepository(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def create(self, *args, **kwargs) -> dict:
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs) -> None:
        pass


class BaseModelRepository(BaseCRUDRepository, metaclass=ABCMeta):
    @abstractmethod
    def get(self, pk: PrimaryKey) -> dict:
        pass

    @abstractmethod
    def create(self, data: RequestPostData) -> dict:
        pass

    @abstractmethod
    def update(self, pk: PrimaryKey, data: RequestPostData):
        pass

    @abstractmethod
    def delete(self, pk: PrimaryKey) -> None:
        pass


class BaseRepository(metaclass=ABCMeta):
    _service: BaseModelService
    _serializer_class: serializers.Serializer
    default_service: BaseModelService | None
    default_serializer_class: serializers.Serializer | None

    def __init__(self,
                 service: BaseModelService = None,
                 serializer_class: serializers.Serializer = None
                 ):
        self._service = service or self.default_service
        self._serializer_class = (serializer_class or
                                  self.default_serializer_class)
