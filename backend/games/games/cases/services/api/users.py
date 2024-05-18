import requests

from django.conf import settings
from django.http.request import HttpRequest

from cases.states.request import DropRequest, FoundsState
from .transfer import CaseData


class UsersApiService:
    routes: dict[str, str] = settings.USERS_MICROSERVICE_ROUTES

    def get_advantage(self, user_request: HttpRequest) -> float:
        advantage = requests.post(
            self.routes.get("get_advantage")
        ).json().get("advantage")

        return float(advantage)
