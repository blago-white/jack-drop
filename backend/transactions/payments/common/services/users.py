import json

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request


class UsersApiService:
    routes = settings.USERS_MICROSERVICE_ROUTES

    def get_info(self, request: Request) -> dict:
        response = requests.get(
            url=self.routes.get("get-info"),
            headers={
                "Authorization": request.headers.get("Authorization")
            }
        )

        print(response.ok, response.json())

        if not response.ok:
            raise ValidationError(code=401)

        return response.json()

    def add_depo(self, amount: float,
                 promocode: str,
                 user_id: int) -> dict:
        body = {
            "amount": amount,
            "user_id": user_id
        }

        if promocode:
            body.update({"promocode": promocode})

        response = requests.post(
            url=self.routes.get("add-depo"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body)
        )

        print(
            "USERS SERVICE DEPO CALLBACK",
            body,
            response.status_code,
            response.json()
        )

        if not response.ok:
            raise ValidationError(detail="Error with adding deposit", code=400)

        return response.json()
