import requests

from games.serializers.upgrade import UpgradeRequestSerializer
from .base import BaseApiService


class UpgradeService(BaseApiService):
    default_endpoint_serializer_class = UpgradeRequestSerializer

    def make_upgrade(self, serialized: UpgradeRequestSerializer) -> bool:
        response = requests.post(
            self._routes.get_user_info("upgrade"),
            data=serialized.data
        ).json()

        return response.get_user_info("success")
