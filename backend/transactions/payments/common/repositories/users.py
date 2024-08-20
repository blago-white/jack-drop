from rest_framework.serializers import Serializer
from rest_framework.request import Request

from .base import BaseRepository

from ..services.users import UsersApiService


class UsersRepository(BaseRepository):
    default_service = UsersApiService()
    default_serializer_class = Serializer

    _service: UsersApiService

    def get_info(self, user_request: Request) -> dict:
        return self._service.get_info(request=user_request)
