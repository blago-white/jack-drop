from django.core.validators import MaxValueValidator, MinValueValidator

from items.config import ITEM_MAX_PRICE, ITEM_MIN_PRICE

__all__ = ["MAX_ITEM_PRICE_VALIDATOR", "MIN_ITEM_PRICE_VALIDATOR"]

MAX_ITEM_PRICE_VALIDATOR = MaxValueValidator(limit_value=ITEM_MAX_PRICE)
MIN_ITEM_PRICE_VALIDATOR = MinValueValidator(limit_value=ITEM_MIN_PRICE)
