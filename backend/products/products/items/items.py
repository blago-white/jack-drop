from dataclasses import dataclass


@dataclass
class ItemInfo:
    """
    Dataclass for holding item data

    :var title: The title of item on market
    :var image_path: The path to item image (recommended on the domain rust.tm)
    :var price: The price of item on market
    """

    title: str
    image_path: str
    price: int
