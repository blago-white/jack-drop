import requests

from games.serializers.site import UpdateDinamicSiteFundsEndpointSerializer
from .base import BaseApiService


class SiteFundsApiService(BaseApiService):
    default_endpoint_serializer_class = UpdateDinamicSiteFundsEndpointSerializer

    def get(self) -> float:
        response = requests.get(
            url=self.default_routes.get("get_funds"),
        )

        print(response.text)

        response = response.json()

        return float(response.get("amount"))

    def update(self, amount: float) -> bool:
        if amount > 0:
            return self.increase(amount=amount)
        return self.decrease(amount=amount)

    def increase(self, amount: float) -> bool:
        response = requests.post(
            url=self.default_routes.get("increase_site_funds"),
            data={
                "delta_amount": amount
            }
        ).json()

        return bool(response.get("ok"))

    def decrease(self, amount: float) -> bool:
        response = requests.post(
            url=self.default_routes.get("decrease_site_funds"),
            data={
                "delta_amount": amount
            }
        ).json()

        return bool(response.get("ok"))
