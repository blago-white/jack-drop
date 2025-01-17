from abc import ABCMeta, abstractmethod

from django.db import models
from django.db import transaction

from accounts.models import Client
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

    @transaction.atomic
    def bulk_inflate_advantages(self) -> bool:
        users: list[Client] = self.get_all()

        for user in users:
            if user.advantage < 0:
                user.advantage = models.Min(
                    models.F("advantage")+(200/24), 0
                )

        self._model.bulk_update(users, ["advantage"])
