from abc import ABCMeta, abstractmethod

from django.db import models

from common.repositories import BaseRepository

from accounts.services.users import UsersService
from accounts.serializers import ClientSerializer


class BaseUsersRepository(BaseRepository, metaclass=ABCMeta):
    default_service = UsersService()
    default_serializer_class = ClientSerializer
    _service: UsersService
    _serializer_class: ClientSerializer

    @abstractmethod
    def get_user_info(self, user_id: int) -> dict:
        pass


class UsersRepository(BaseUsersRepository):
    def get_user_info(self, user_id: int) -> dict:
        user = self._service.get_user_info(user_id=user_id)

        serialized: ClientSerializer = self._serializer_class(instance=user)

        return serialized.data