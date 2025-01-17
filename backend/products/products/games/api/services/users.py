import json

import requests
from django.conf import settings
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed

code = 401
from games.serializers.users import GetUserInfoEndpointSerializer
from common.services.api.base import BaseApiService


class UsersApiService(BaseApiService):
    default_endpoint_serializer_class = GetUserInfoEndpointSerializer
    routes: dict[str, str] = settings.USERS_MICROSERVICE_ROUTES

    def get_user_info(
            self, user_request: Request = None,
            jwt: str = None) -> dict:
        if user_request:
            return self.send_auth_get_api_request(
                path=self.routes.get("get_info"),
                user_request=user_request
            )

        return self.send_auth_get_api_request(
            path=self.routes.get("get_info"),
            auth_header=jwt
        )

    def get_user_by_id(self, user_id: int):
        response = requests.get(self.routes.get("get_info_by_id").format(
            client_id=user_id
        ), headers={}, data={})

        if not response.ok:
            raise Exception("Error getting user info")

        return response.json()

    def get_users_info(self, users_ids: list[int]) -> tuple[bool, list]:
        response = requests.get(
            url=self.routes.get("bulk_get_info"),
            data=json.dumps({"users": users_ids}),
            headers={
                "Content-Type": "application/json"
            }
        )

        return response.json()

    def update_user_balance_by_request(
            self, delta_amount: int,
            user_id: int = None,
            user_request: int = None) -> bool:
        if user_id:
            path = self.routes.get("update_balance").format(
                client_id=user_id
            )
        elif user_request:
            path = self.routes.get("update_balance_jwt"),

        else:
            raise AuthenticationFailed()

        response = requests.patch(
            url=path,
            data={
                "delta_amount": delta_amount
            }
        ).json()

        return response

    def update_user_balance_by_id(
            self, delta_amount: int,
            user_id: int,
    ) -> bool:
        response = requests.patch(
            url=self.routes.get("update_balance").format(
                client_id=user_id
            ),
            data={"delta_amount": delta_amount}
        )

        return response.json().get("ok")

    def update_user_hiden_balance(
            self, user_id: int,
            delta_amount: float):
        response = requests.patch(
            url=self.routes.get("update_hidden_balance").format(
                client_id=user_id
            ),
            data={"delta_amount": delta_amount}
        ).json()

        return response.get("ok")

    def add_user_lose(
            self, user_request: Request,
            advantage_diff: float) -> tuple[bool, float]:
        header = user_request.headers.get(
            "Authorization"
        )

        response = requests.post(
            url=self.routes.get("add_user_lose"),
            headers={
                "Authorization": header
            },
            data={"advantage_diff": advantage_diff}
        ).json()

        return response.get("ok"), float(response.get("user_advantage"))

    def update_user_advantage(self, delta_advantage: float,
                              user_id: int = None,
                              user_request: Request = None
                              ) -> tuple[bool, float]:
        if user_id:
            response = requests.put(
                url=self.routes.get("update_advantage_by_id").format(
                    user_id=user_id
                ),
                data={"delta_advantage": delta_advantage}
            ).json()

        else:
            response = requests.put(
                url=self.routes.get("update_advantage"),
                headers={"Authorization": user_request.headers.get(
                    "Authorization"
                )},
                data={"delta_advantage": delta_advantage}
            ).json()

        return response.get("ok"), float(response.get("to_blogger"))

    @staticmethod
    def send_auth_get_api_request(
            path: str,
            user_request: Request = None,
            auth_header: str = None
    ) -> dict:
        if not (user_request or auth_header):
            raise AuthenticationFailed()

        auth_header = (
            user_request.headers.get("Authorization")
        ) if auth_header is None else (
            auth_header
        )
        response = requests.get(
            path,
            headers={"Authorization": auth_header},
        )

        if (not response.ok) or (response.status_code in (401, 403)):
            raise AuthenticationFailed()

        return response.json()

    @staticmethod
    def send_auth_patch_api_request(
            path: str,
            user_request: Request = None,
            auth_header: str = None,
            data: dict = None
    ) -> dict:
        if not (user_request or auth_header):
            print("NO HEADER")

            raise AuthenticationFailed()

        if not auth_header:
            auth_header = user_request.headers.get("Authorization")

        response = requests.patch(
            path,
            headers={"Authorization": auth_header},
            data=data or {}
        )

        if (not response.ok) or (response.status_code in (401, 403)):
            print("NO RESPONSE")

            raise AuthenticationFailed()

        return response.json()
