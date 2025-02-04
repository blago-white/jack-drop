import requests

from games.serializers.site import UpdateDinamicSiteFundsEndpointSerializer
from common.services.api.base import BaseApiService


class SiteFundsApiService(BaseApiService):
    default_endpoint_serializer_class = UpdateDinamicSiteFundsEndpointSerializer

    def get(self) -> float:
        result = self._get()

        return float(result.get("amount"))

    def get_all(self) -> dict[str, float]:
        return self._get()

    def get_for_cases(self) -> float:
        result = self._get()

        return float(result.get("amount_cases"))

    def update(self, amount: float, for_cases: bool = False) -> bool:
        if amount > 0:
            return self.increase(amount=amount, for_cases=for_cases)
        return self.decrease(amount=amount, for_cases=for_cases)

    def increase(self, amount: float, for_cases: bool = False) -> bool:
        response = requests.post(
            url=self.default_routes.get("increase_site_funds"),
            data={
                "delta_amount": amount,
                "for_cases": for_cases
            }
        ).json()

        return bool(response.get("ok"))

    def decrease(self, amount: float, for_cases: bool = False) -> bool:
        response = requests.post(
            url=self.default_routes.get("decrease_site_funds"),
            data={
                "delta_amount": amount,
                "for_cases": for_cases
            }
        ).json()

        return bool(response.get("ok"))

    def _get(self):
        response = requests.get(
            url=self.default_routes.get("get_funds"),
        )

        response = response.json()

        return response