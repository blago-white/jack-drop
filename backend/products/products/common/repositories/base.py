from abc import ABCMeta, abstractmethod

from rest_framework import serializers

from common.services import base

RequestPostData = dict[str, int | str]
PrimaryKey = int


class BaseRepository(metaclass=ABCMeta):
    @property
    @abstractmethod
    def _service(self) -> base.BaseModelService:
        pass

    @property
    @abstractmethod
    def _serializer(self) -> serializers.Serializer:
        pass

    @abstractmethod
    def get_all(self, *args, **kwargs) -> dict:
        pass

    @abstractmethod
    def get(self, *args, **kwargs) -> dict:
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


class BaseModelRepository(BaseRepository, metaclass=ABCMeta):
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
