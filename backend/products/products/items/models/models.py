from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.base import BaseImageModel
from common.models.mixins import TitleModelMixin
from market.services.items import MarketItemParser
from . import validators


class Item(TitleModelMixin, BaseImageModel):
    market_link = models.URLField(verbose_name=_(
                                      "URL of this products on rust.rm"
                                  ),
                                  blank=False,
                                  default="unknown")

    title = models.CharField(verbose_name=_("Item title"),
                             max_length=100,
                             blank=True)
    image_path = models.URLField(verbose_name=_("Item image path"),
                                 blank=True)
    price = models.FloatField(verbose_name=_("Price of item"),
                              validators=[
                                  validators.MAX_ITEM_PRICE_VALIDATOR,
                                  validators.MIN_ITEM_PRICE_VALIDATOR
                              ],
                              blank=True)
    hash_name = models.CharField(verbose_name="Hash name", null=True, blank=True)

    class Meta:
        db_table = "items_items"

    def __init__(self, *args,
                 market_parser: MarketItemParser = MarketItemParser(),
                 **kwargs):
        self._market_parser = market_parser

        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{super().__str__()} ({self.price} РУБ)"

    def save(
            self, force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self._update_fields()

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def _update_fields(self) -> None:
        item_info = self._market_parser.get_info(self.market_link)

        self.title = item_info.title
        self.image_path = item_info.image_path
        self.price = item_info.price
        self.hash_name = item_info.market_hash_name

    def _get_image(self) -> models.URLField:
        return self.image_path
