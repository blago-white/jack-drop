import json

import requests
from rest_framework.exceptions import ValidationError

from games.serializers.battle import BattleRequestServiceEndpointSerializer, \
    MakeBattleServiceEndpointSerializer
from common.services.api.base import BaseApiService


class BattleRequestApiService(BaseApiService):
    default_endpoint_serializer_class = BattleRequestServiceEndpointSerializer

    def create(self, serialized: BattleRequestServiceEndpointSerializer) -> bool:
        response = requests.post(
            self._routes.get("create_battle_request"),
            data=serialized.data
        )

        try:
            return response.json().get("ok") if (
                    response.status_code == 201
            ) else False
        except requests.exceptions.JSONDecodeError:
            raise ValidationError("Error with creating battle")

    def get_by_case(self, case_id: int) -> list[dict]:
        response = requests.get(
            self._routes.get("get_battle_requests").format(
                case_id=case_id
            ),
        ).json()

        return response

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
        response = requests.post(
            url=self._routes.get("make_battle"),
            data=json.dumps(serialized.data),
            headers={
                "Content-Type": "application/json"
            }
        )

        try:
            if not response.ok:
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
            url=self._routes.get("get_battles").format(
                user_id=user_id
            ),
        )

        return response.json()

    def get_count_by_case(self):
        response = requests.get(
            url=self._routes.get("get_battle_requests_count"),
        )

        return response.json()
