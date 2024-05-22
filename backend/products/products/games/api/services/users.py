import requests
from django.conf import settings
from rest_framework.request import Request

from games.serializers.users import GetUserInfoEndpointSerializer
from .base import BaseApiService


class UsersApiService(BaseApiService):
    default_endpoint_serializer_class = GetUserInfoEndpointSerializer
    routes: dict[str, str] = settings.USERS_MICROSERVICE_ROUTES

    def get(self, user_request: Request) -> dict:
        return self.send_auth_get_api_request(
            path=self.routes.get("get_info"),
            user_request=user_request
        )

    @staticmethod
    def send_auth_get_api_request(path: str, user_request: Request) -> dict:
        auth_header = user_request.auth

        return requests.get(
            path,
            headers={"Authorization": auth_header}
        ).json()
