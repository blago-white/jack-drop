from abc import ABCMeta, abstractmethod

from django.db import models
from django.contrib.auth import get_user_model

from common.services import BaseService
from accounts.models import Client


class BaseUsersService(BaseService, metaclass=ABCMeta):
    default_model = Client

    @abstractmethod
    def get_user_info(self, user_id: int) -> models.Model:
        pass


class UsersService(BaseUsersService):
    def get_user_info(self, user_id: int) -> models.Model:
        return self._model.objects.get(pk=user_id)
