import json

import requests

from games.serializers.upgrade import UpgradeRequestSerializer
from .base import BaseApiService


class UpgradeService(BaseApiService):
    default_endpoint_serializer_class = UpgradeRequestSerializer

    def make_upgrade(self, serialized: UpgradeRequestSerializer) -> bool:
        response = requests.post(
            self._routes.get("upgrade"),
            data=json.dumps(serialized.data),
            headers={"Content-Type": "application/json"}
        )

        return response.json().get("success")
