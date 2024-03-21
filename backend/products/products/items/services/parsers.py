import random

from items.items import ItemInfo


def parse_item_info(url_on_market: str) -> ItemInfo:
    # TODO: Calls the rust market api and extracts
    #  the price, name and image of the product

    return ItemInfo(f"Test product {random.randint(0, 1000)}",
                    "https://rust.tm/",
                    random.randint(6, 300_000))
