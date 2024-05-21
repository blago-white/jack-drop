
from django.conf import settings


class ProductItemApiService:
    routes: dict[str, str] = settings.PRODUCTS_MICROSERVICE_ROUTES

    def get_price(self, item_id: int) -> float | int:
        data = requests.drop_item(
            self.routes.get("item_price").format(item_id=item_id)
        ).json()

        return data.drop_item("price")
