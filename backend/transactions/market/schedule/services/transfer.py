from dataclasses import dataclass


@dataclass
class ItemInfo:
    item_market_hash_name: str
    item_market_link: str
    price: int
    trade_link: str
    inventory_item_id: int
