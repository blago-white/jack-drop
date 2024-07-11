from abc import ABCMeta, abstractmethod

from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import ClientSerializer
from accounts.services.users import UsersService
from common.repositories import BaseRepository


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

    def create(self, steam_uid: int) -> dict:
        result = self._service.create(
            steam_id=steam_uid,
            username="testuser"
        )  # TODO: Get username

        refresh = RefreshToken.for_user(user=result)

        return {
            "refresh": str(refresh),
            "access": refresh.access_token
        }
