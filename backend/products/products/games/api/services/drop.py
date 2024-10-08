import json

import requests

from games.serializers.drop import DropCaseRequestSerializer
from common.services.api.base import BaseApiService


class CaseDropApiService(BaseApiService):
    default_endpoint_serializer_class = DropCaseRequestSerializer

    def drop(self, serialized: dict) -> dict:
        response = requests.post(
            self._routes.get("drop"),
            data=json.dumps(serialized),
            headers={
                "Content-Type": "application/json"
            }
        )

        print("DROP RESP", response.text)
        print("DROP PLD", serialized)

        return response.json()
