from abc import ABCMeta, abstractmethod

from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

from accounts.serializers import PrivateClientSerializer, PublicClientSerializer
from accounts.services.users import UsersService
from accounts.services.steam import SteamAccountsService
from accounts.models.client import Client
from accounts.services.lottery import LotteryWinsModelService
from balances.serivces.balance import ClientBalanceService
from balances.serivces.deposits import DepositsService

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
    default_deposits_service = DepositsService()

    default_serializer_class = PrivateClientSerializer
    _serializer_class: PrivateClientSerializer

    def __init__(self, *args,
                 balance_service: ClientBalanceService = None,
                 steam_service: SteamAccountsService = None,
                 deposits_service: DepositsService = None,
                 **kwargs):
        self._balance_service = balance_service or self.default_balance_service
        self._steam_service = steam_service or self.default_steam_service
        self._deposits_service = deposits_service or self.default_deposits_service

        super().__init__(*args, **kwargs)

    def get_user_info(self, user_id: int) -> dict:
        try:
            user: Client = self._service.get_user_info(user_id=user_id)
        except:
            raise ValidationError(code=404)

        serialized: PrivateClientSerializer = self._serializer_class(
            instance={
                "id": user.id,
                "steam_id": user.steam_id,
                "username": user.username,
                "avatar": user.avatar,
                "advantage": user.advantage,
                "trade_link": user.trade_link,
                "displayed_balance": self._balance_service.get_balance(
                    client_id=user.id
                ).displayed_balance,
                "has_deposits": self._deposits_service.has_deposits(
                    user_id=user_id
                )
            }
        )

        return serialized.data

    def get_users_info(self, users_ids: list[int]) -> dict:
        complete, users = self._service.get_users_info(users_ids=users_ids)

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

    def create(self, steam_uid: int) -> tuple[int, dict]:
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
    default_lottery_service = LotteryWinsModelService()
    default_serializer_class = PublicClientSerializer
    _serializer_class: PublicClientSerializer

    def __init__(self, *args,
                 balance_service: ClientBalanceService = None,
                 lottery_service: LotteryWinsModelService = None,
                 **kwargs):
        self._balance_service = balance_service or self.default_balance_service
        self._lottery_service = lottery_service or self.default_lottery_service

        super().__init__(*args, **kwargs)

    def get_user_info(self, user_id: int) -> dict:
        try:
            user = self._service.get_user_info(user_id=user_id)
        except:
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
                "lottery_wins_list": self._lottery_service.retrieve_list_unviewed_prizes(
                    client_id=user.id
                ),
                "is_blogger": user.referral.is_blogger
            }
        )

        return serialized.data

    def update_trade_link(self, user_id: int, trade_link: str):
        self._service.update_trade_link(user_id=user_id, trade_link=trade_link)

        return {"ok": True, "link": trade_link}
