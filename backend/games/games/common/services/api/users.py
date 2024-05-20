import requests

from django.conf import settings
from rest_framework.request import Request

from .transfer import UserData


class UsersApiService:
    routes: dict[str, str] = settings.USERS_MICROSERVICE_ROUTES

    def get_advantage(self, user_request: Request) -> float:
        advantage = self.make_auth_get_api_request(
            path=self.routes.get("get_advantage"),
            user_request=user_request
        ).get("advantage")

        return float(advantage)

    def get_info(self, user_request: Request) -> UserData:
        data = self.make_auth_get_api_request(
            path=self.routes.get("get_info"),
            user_request=user_request
        )

        return UserData(
            id=data.get("id"),
            advantage=data.get("advantage")
        )

    @staticmethod
    def make_auth_get_api_request(path: str, user_request: Request) -> dict:
        auth_header = user_request.auth

        return requests.get(
            path,
            headers={"Authorization": auth_header}
        ).json()
