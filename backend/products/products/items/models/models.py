from django.db import models

from common.models.mixins import TitleModelMixin

from . import validators


class Item(TitleModelMixin, models.Model):
    title = models.CharField(verbose_name="Item title",
                             max_length=100)
    image = models.ImageField(verbose_name="Item image")
    price = models.FloatField(verbose_name="Price of item",
                              validators=[
                                  validators.MAX_ITEM_PRICE_VALIDATOR,
                                  validators.MIN_ITEM_PRICE_VALIDATOR
                              ])

    class Meta:
        db_table = "items_items"
