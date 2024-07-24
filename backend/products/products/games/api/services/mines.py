import json

import requests

from games.serializers.mines import MinesGameRequestSerializer
from common.services.api.base import BaseApiService


class MinesGameApiService(BaseApiService):
    default_endpoint_serializer_class = MinesGameRequestSerializer

    def make(self, serialized: MinesGameRequestSerializer):
        response = requests.post(
            self._routes.get("make_mines_game"),
            data=json.dumps(serialized.data),
            headers={"Content-Type": "application/json"}
        )

        print("MAKE MINES RESPONSE", response.text, serialized.data)

        return response.json()

    def next(self, user_id: int, site_funds: float):
        response = requests.post(
            self._routes.get("next_mines_game"),
            data={
                "user_id": user_id,
                "site_funds": {
                    "site_active_funds": site_funds
                }
            },
            headers={"Content-Type": "application/json"}
        )

        print("MAKE MINES RESPONSE", response.text, serialized.data)

        return response.json()

    def stop(self, user_id: int):
        response = requests.post(
            self._routes.get("stop_mines_game"),
            data={
                "user_id": user_id,
            },
            headers={"Content-Type": "application/json"}
        )

        print("MAKE MINES RESPONSE", response.text, serialized.data)

        return response.json()
