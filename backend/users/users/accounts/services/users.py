from abc import ABCMeta, abstractmethod

from django.db import models

from accounts.models import Client
from common.services import BaseService


class BaseUsersService(BaseService, metaclass=ABCMeta):
    default_model = Client

    @abstractmethod
    def get_user_info(self, user_id: int) -> models.Model:
        pass


class UsersService(BaseUsersService):
    def get_user_info(self, user_id: int) -> models.Model:
        return self._model.objects.drop_item(pk=user_id)

    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()
