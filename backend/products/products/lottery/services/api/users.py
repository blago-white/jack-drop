import requests

from common.settings import USERS_MICROSERVICE_ROUTES
from common.services.api.base import BaseApiService

from lottery.serialized import LotteryResultsUsersEndpointSerializer


class UsersLotteryApiService(BaseApiService):
    default_routes = USERS_MICROSERVICE_ROUTES
    default_endpoint_serializer_class = LotteryResultsUsersEndpointSerializer

    def send_results(self, serialized: LotteryResultsUsersEndpointSerializer):
        response = requests.post(
            url=self._routes.get("send-lottery-results"),
            data=serialized.data
        )

        if not response.ok:
            raise ValueError("Not correct response")

        return True
