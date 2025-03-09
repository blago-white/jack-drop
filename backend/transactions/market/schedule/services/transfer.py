from dataclasses import dataclass


@dataclass
class ItemInfo:
    item_market_hash_name: str
    item_market_link: str
    owner_id: int
    price: int
    trade_link: str
    inventory_item_id: int
