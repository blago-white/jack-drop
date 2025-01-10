from typing import Collection

from abc import ABCMeta, abstractmethod

from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

from accounts.serializers import PrivateClientSerializer, PublicClientSerializer
from accounts.services.users import UsersService
from accounts.services.steam import SteamAccountsService
from balances.serivces.balance import ClientBalanceService

from common.repositories import BaseRepository


class BaseUsersRepository(BaseRepository, metaclass=ABCMeta):
    default_service = UsersService()
    _service: UsersService

    @abstractmethod
    def get_user_info(self, user_id: int) -> dict:
        pass


class PrivateUsersRepository(BaseUsersRepository):
    default_balance_service = ClientBalanceService()
    default_steam_service = SteamAccountsService()

    default_serializer_class = PrivateClientSerializer
    _serializer_class: PrivateClientSerializer

    def __init__(self, *args,
                 balance_service: ClientBalanceService = None,
                 steam_service: SteamAccountsService = None,
                 **kwargs):
        self._balance_service = balance_service or self.default_balance_service
        self._steam_service = steam_service or self.default_steam_service

        super().__init__(*args, **kwargs)

    def get_user_info(self, user_id: int) -> dict:
        try:
            user = self._service.get_user_info(user_id=user_id)
        except:
            raise ValidationError(code=404)

        serialized: PrivateClientSerializer = self._serializer_class(
            instance={
                "id": user.id,
                "username": user.username,
                "avatar": user.avatar,
                "advantage": user.advantage,
                "trade_link": user.trade_link,
                "displayed_balance": self._balance_service.get_balance(
                    client_id=user.id
                ).displayed_balance
            }
        )

        return serialized.data

    def get_users_info(self, users_ids: list[int]) -> dict:
        complete, users = self._service.get_users_info(users_ids=users_ids)

        print(complete, users, "USERS LIST DATA", users_ids)

        return {
            "full": complete,
            "users": self._serializer_class(instance=users, many=True).data
        }

    def get_user_info_by_jwt(self, request: Request) -> dict:
        return self.get_user_info(user_id=request.user.id)

    def get(self, steam_id: int) -> dict | None:
        try:
            user = self._service.get_user_info_by_steam(steam_id=steam_id)

            refresh = RefreshToken.for_user(user=user)

            return {
                "refresh": str(refresh),
                "access": refresh.access_token
            }
        except:
            return

    def create(self, steam_uid: int) -> Collection[int, dict]:
        result = self._service.create(
            steam_id=steam_uid,
            username=self._steam_service.get_username(steam_id=steam_uid),
            avatar_url=self._steam_service.get_avatar(steam_id=steam_uid)
        )

        refresh = RefreshToken.for_user(user=result)

        return result.id, {
            "refresh": str(refresh),
            "access": refresh.access_token
        }


class PublicUsersRepository(BaseUsersRepository):
    default_balance_service = ClientBalanceService()
    default_serializer_class = PublicClientSerializer
    _serializer_class: PublicClientSerializer

    def __init__(self, *args,
                 balance_service: ClientBalanceService = None,
                 **kwargs):
        self._balance_service = balance_service or self.default_balance_service

        super().__init__(*args, **kwargs)

    def get_user_info(self, user_id: int) -> dict:
        try:
            user = self._service.get_user_info(user_id=user_id)
        except:
            print()
            raise ValidationError(code=403)

        serialized: PublicClientSerializer = self._serializer_class(
            instance={
                "id": user.pk,
                "username": user.username,
                "avatar": user.avatar,
                "trade_link": user.trade_link,
                "displayed_balance": self._balance_service.get_balance(
                    client_id=user.id
                ).displayed_balance,
                "is_blogger": user.referral.is_blogger
            }
        )

        return serialized.data

    def update_trade_link(self, user_id: int, trade_link: str):
        self._service.update_trade_link(user_id=user_id, trade_link=trade_link)

        return {"ok": True, "link": trade_link}
