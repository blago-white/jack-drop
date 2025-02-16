from abc import ABCMeta, abstractmethod

from django.db import models
from django.db import transaction

from accounts.models.client import Client, ClientAdvantage
from common.services import BaseService


class BaseUsersService(BaseService, metaclass=ABCMeta):
    default_model = Client

    @abstractmethod
    def get_user_info(self, user_id: int) -> models.Model:
        pass


class UsersService(BaseUsersService):
    def get_user_info(self, user_id: int) -> models.Model:
        return self._model.objects.get(pk=user_id)

    def get_user_info_by_steam(self, steam_id: int) -> models.Model:
        return self._model.objects.get(steam_id=steam_id)

    def get_all(self) -> models.QuerySet:
        return self._model.objects.all()

    def update_trade_link(self, user_id: int, trade_link: str):
        return self._model.objects.filter(pk=user_id).update(
            trade_link=trade_link
        )

    def create(self, steam_id: int, username: str, avatar_url: str = None):
        return self._model.objects.create(
            steam_id=steam_id,
            username=username,
            avatar=avatar_url
        )

    def get_users_info(self, users_ids: list[int]) -> models.QuerySet:
        qs = self._model.objects.filter(pk__in=users_ids)

        return len(users_ids) == len(qs), qs
