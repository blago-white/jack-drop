import requests

from games.serializers.battle import BattleRequestServiceEndpointSerializer, \
    MakeBattleServiceEndpointSerializer
from .base import BaseApiService


class BattleRequestApiService(BaseApiService):
    default_endpoint_serializer_class = BattleRequestServiceEndpointSerializer

    def create(self, serialized: BattleRequestServiceEndpointSerializer) -> bool:
        response = requests.post(
            self._routes.get("create_battle_request"),
            data=serialized.data
        ).json()

        return response.get("ok")

    def cancel(self, initiator_id: int) -> bool:
        response = requests.delete(
            self._routes.get("drop_battle_request").format(
                initiator_id=initiator_id
            ),
        ).json()

        return response.get("ok")


class BattleApiService(BaseApiService):
    default_endpoint_serializer_class = MakeBattleServiceEndpointSerializer

    def make(self, serialized: MakeBattleServiceEndpointSerializer):
        response = requests.post(
            self._routes.get("make_battle"),
            data=serialized.validated_data
        ).json()

        return response.get("ok")
