import requests

from django.http.request import HttpRequest
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class UsersService:
    _routes = settings.USERS_MICROSERVICE_ROUTES

    def get_username(self, request: HttpRequest) -> str:
        return self.get(request=request).get("username")

    def get(self, request: HttpRequest):
        jwt = request.headers.get("Authorization")

        response = requests.get(
            url=self._routes.get("get_info"),
            headers={"Authorization": jwt}
        )

        print("AUTH REQ", response.ok, response.text, response.status_code)

        if not response.ok:
            raise AuthenticationFailed()

        return response.json()
