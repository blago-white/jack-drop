from django.db import models
from . import validators


class Item(models.Model):
    title = models.CharField(verbose_name="Item title",
                             max_length=100)
    image = models.ImageField(verbose_name="Item image")
    price = models.IntegerField(
        verbose_name="Price of item",
        validators=[
            validators.MAX_ITEM_PRICE_VALIDATOR,
            validators.MIN_ITEM_PRICE_VALIDATOR
        ]
    )
