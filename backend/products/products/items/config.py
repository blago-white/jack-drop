ITEM_TITLE_MAX_LENGTH = 100
ITEM_MAX_PRICE = 500000
ITEM_MIN_PRICE = 0.0001

MAIN_RETRIEVE_ITEM_URL = "https://rust.tm/api/ItemInfo/{classid}_{instanceid}/en/"

MAIN_RETRIEVE_ITEM_IMAGE_URL = "https://cdn.rust.tm/item/{name}/300.png"

__all__ = [i for i in globals() if i[0] != "_"]
