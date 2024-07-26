from rest_framework.request import Request

from common.repositories.base import BaseRepository

from ..services.users import UsersService


class UsersApiRepository(BaseRepository):
    default_service = UsersService()
    default_serializer_class = None

    _service: UsersService

    def get(self, user_request: Request) -> dict:
        return self._service.get(request=user_request)

    def get_username(self, user_request: Request) -> dict:
        return self._service.get_username(request=user_request)
