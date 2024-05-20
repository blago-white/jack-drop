
from django.conf import settings

from cases.states.request import DropRequest
from .transfer import CaseData, CaseItem


class ProductItemApiService:
    routes: dict[str, str] = settings.PRODUCTS_MICROSERVICE_ROUTES

    def get_price(self, item_id: int) -> float | int:
        data = requests.get(
            self.routes.get("item_price").format(item_id=item_id)
        ).json()

        return data.get("price")
