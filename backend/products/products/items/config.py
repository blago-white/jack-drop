__all__ = ["ITEM_MIN_PRICE",
           "ITEM_MAX_PRICE",
           "ITEM_TITLE_MAX_LENGTH",
           "MAIN_RETRIEVE_ITEM_URL"]

ITEM_TITLE_MAX_LENGTH = 100
ITEM_MAX_PRICE = 500000
ITEM_MIN_PRICE = 0.0001

MAIN_RETRIEVE_ITEM_URL = """https://rust.tm/api/ItemInfo/{classid}_{instanceid}/en/"""
