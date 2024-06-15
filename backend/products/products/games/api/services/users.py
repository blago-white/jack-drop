import requests
from django.conf import settings
from rest_framework.request import Request

from games.serializers.users import GetUserInfoEndpointSerializer
from .base import BaseApiService


class UsersApiService(BaseApiService):
    default_endpoint_serializer_class = GetUserInfoEndpointSerializer
    routes: dict[str, str] = settings.USERS_MICROSERVICE_ROUTES

    def get_user_info(self, user_request: Request = None,
                      jwt: str = None) -> dict:
        # TODO: Remove on deploy

        return {
            "id": 1,
            "user_advantage": -200,
            "displayed_balance": 1000,
        }

        if user_request:
            return self.send_auth_get_api_request(
                path=self.routes.get("get_info"),
                user_request=user_request
            )

        return self.send_auth_get_api_request(
            path=self.routes.get("get_info"),
            auth_header=jwt
        )

    def update_user_balance(self, delta_amount: int,
                            user_id: int = None,
                            user_request: int = None) -> bool:
        serialized = self._endpoint_serializer_class(
            instance={
                "delta_amount": delta_amount
            }
        )

        if user_id:
            return self.send_auth_patch_api_request(
                path=self.routes.get("update_balance").format(
                    client_id=user_request
                ),
                user_request=user_request,
                data=serialized.data
            ).get("ok")
        elif user_request:
            return self.send_auth_patch_api_request(
                path=self.routes.get("update_balance_jwt"),
                user_request=user_request,
                data=serialized.data
            ).get("ok")

    @staticmethod
    def send_auth_get_api_request(
            path: str,
            user_request: Request = None,
            auth_header: str = None
    ) -> dict:
        auth_header = user_request.auth if auth_header is None else auth_header

        return requests.get(
            path,
            headers={"Authorization": auth_header},
        ).json()

    @staticmethod
    def send_auth_patch_api_request(
            path: str,
            user_request: Request,
            data: dict = None
    ) -> dict:
        # TODO: Remove on deploy
        return {}

        auth_header = user_request.auth

        return requests.patch(
            path,
            headers={"Authorization": auth_header},
            data=data or {}
        ).json()
