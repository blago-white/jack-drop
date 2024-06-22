import requests
import json

from .base import BaseApiService

from games.serializers.fortune import PrizeTypeRequestSerializer, PrizeRequestSerializer


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
        print(serialized.data, "EERRRORRSSSSSSS")

        response = requests.get(
            self._routes.get("get_prize_type_wheel"),
            data=json.dumps(serialized.data),
            headers={
                "Content-Type": "application/json"
            }
        )

        print(response.text, "EEELELL")

        return response.json()


class FortuneWheelPrizeApiService(BaseApiService):
    default_endpoint_serializer_class = PrizeRequestSerializer

    def make_prize(self, serialized: PrizeRequestSerializer) -> dict:
        print(serialized.data, "EERRRORR")

        response = requests.post(
            self._routes.get("get_prize_wheel"),
            data=json.dumps(serialized.data),
            headers={
                "Content-Type": "application/json"
            }
        )

        print(response.text, "EERRRRR")

        return response.json()
