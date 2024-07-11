import json

import requests

from games.serializers.fortune import (PrizeTypeRequestSerializer,
                                       PrizeRequestSerializer,
                                       TimeoutRequestSerializer)
from .base import BaseApiService


class PrizeTypes:
    PROMOCODE = "P"
    CONTRACT = "C"
    FREE_SKIN = "F"
    CASE_DISCOUNT = "D"
    UPGRADE = "U"


FREE_SKIN_PRICE_RANGE = (20, 1000)
GAME_SKIN_PRICE_RANGE = (100, 500)


class FortuneWheelPrizeTypeApiService(BaseApiService):
    default_endpoint_serializer_class = PrizeTypeRequestSerializer

    def get_prize_type(self, serialized: PrizeTypeRequestSerializer) -> dict:
        response = requests.get(
            self._routes.get("get_prize_type_wheel"),
            data=json.dumps(serialized.data),
            headers={
                "Content-Type": "application/json"
            }
        )

        return response.json()


class FortuneWheelPrizeApiService(BaseApiService):
    default_endpoint_serializer_class = PrizeRequestSerializer

    def make_prize(self, serialized: PrizeRequestSerializer) -> dict:
        response = requests.post(
            self._routes.get("get_prize_wheel"),
            data=json.dumps(serialized.data),
            headers={
                "Content-Type": "application/json"
            }
        )

        return response.json()

    def use_promocode(self, user_id: int, promocode: str) -> bool:
        response = requests.post(
            self._routes.get("use_fortune_promo"),
            data=json.dumps({
                "user_id": user_id,
                "promocode": promocode
            }),
            headers={
                "Content-Type": "application/json"
            }
        )

        return response.ok


class FortuneWheelTimeoutApiService(BaseApiService):
    default_endpoint_serializer_class = TimeoutRequestSerializer

    def get(self, serialized: TimeoutRequestSerializer) -> int:
        response = requests.get(
            self._routes.get("get_timeout_wheel").format(
                user_id=serialized.data.get("user_id")
            ),
        )

        return response.json()
