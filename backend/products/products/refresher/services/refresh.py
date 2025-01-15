from market.services.items import MarketItemParser
from items.services.items import ItemService
from items.models.models import Item


def refresh_prices(
        market_api_service: MarketItemParser = MarketItemParser(),
        items_service: ItemService = ItemService()
) -> None:
    items: list[Item] = items_service.get_all()

    items_prices = market_api_service.bulk_get_prices(
        [i.market_link for i in items]
    )

    for item, price in zip(items, items_prices, strict=True):
        item.price = price

    items_service.bulk_set_price(items=items)
