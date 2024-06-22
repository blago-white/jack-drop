import json

import requests

from games.serializers.mines import MinesGameRequestSerializer
from .base import BaseApiService


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
