from market.services.items import MarketItemParser
from items.services.items import ItemService
from items.models.models import Item


@shared_task
def refresh_prices(
        market_api_service: MarketItemParser = MarketItemParser(),
        items_service: ItemService = ItemService()
) -> None:
    item: Item

    for item in items_service.get_all():
        new_price = market_api_service.get_info(url=item.market_link).price

        items_service.set_price(item_id=item.pk, item_price=new_price)
