import json
import requests

from requests.exceptions import JSONDecodeError
from rest_framework.exceptions import ValidationError

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

        print("EERRRRRRRRRRRRRRRRRRRRRRRRRRR")

        try:
            print(response.json(), "RESPONSE")

            return response.json().get("ok") if (
                    response.status_code == 201
            ) else False
        except requests.exceptions.JSONDecodeError:
            raise ValidationError("Error with creating battle")

    def cancel(self, initiator_id: int) -> bool:
        response = requests.delete(
            self._routes.get("drop_battle_request").format(
                initiator_id=initiator_id
            ),
        ).json()

        return response.get("ok")


class BattleApiService(BaseApiService):
    default_endpoint_serializer_class = MakeBattleServiceEndpointSerializer

    def make(self, serialized: MakeBattleServiceEndpointSerializer) -> (
            dict | bool
    ):
        print("MAKE REQUEST:", serialized.data)

        response = requests.post(
            url=self._routes.get("make_battle"),
            data=json.dumps(serialized.data),
            headers={
                "Content-Type": "application/json"
            }
        )

        try:
            print("MAKE RESULT:", response.json(), "|", response.status_code)
            if response.status_code not in (201, 200):
                raise ValueError()

            return response.json()
        except:
            return False

    def get_stats(self, user_id: int) -> dict:
        response = requests.get(
            url=self._routes.get("get_battle_stats").format(user_id=user_id),
        )

        return response.json()

    def get_all(self, user_id: int) -> dict:
        response = requests.get(
            url=self._routes.get("get_battles").format(user_id=user_id),
        )

        return response.json()
