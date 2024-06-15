from django.core.validators import MaxValueValidator, MinValueValidator

from cases.config import MAX_CHANSE_PERCENT, MIN_CHANSE_PERCENT

__all__ = ["MIN_CHANCE_VALUE_VALIDATOR", "MAX_CHANCE_VALUE_VALIDATOR"]


MAX_CHANCE_VALUE_VALIDATOR = MaxValueValidator(MAX_CHANSE_PERCENT)

MIN_CHANCE_VALUE_VALIDATOR = MinValueValidator(MIN_CHANSE_PERCENT)
