import requests
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from django.conf import settings


class UsersApiService:
    routes = settings.USERS_MICROSERVICE_ROUTES

    def get_info(self, request: Request) -> dict:
        response = requests.get(
            url=self.routes.get("get-info"),
            headers={
                "Authorization": request.headers.get("Authorization")
            }
        )

        if not response.ok:
            raise ValidationError(code=401)

        return response.json()
