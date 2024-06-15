import json
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
        )

        print(response.json(), "RESPONSE")

        return response.json().get("ok") if (
                response.status_code == 201
        ) else False

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
        print("MAKE REQUEST:", serialized.data)

        response = requests.post(
            url=self._routes.get("make_battle"),
            json=json.dumps(dict(serialized.data)),
            headers={
                "Content-Type": "application/json"
            }
        )

        print("MAKE RESULT:", response.json())

        try:
            return response.json()
        except:
            return False
