import requests

from games.serializers.drop import DropCaseRequestSerializer
from .base import BaseApiService


class CaseDropApiService(BaseApiService):
    default_endpoint_serializer_class = DropCaseRequestSerializer

    def drop(self, serialized: dict) -> dict:
        response = requests.post(
            self._routes.get_user_info("drop"),
            data=serialized
        )

        return response.json()
