from django.db import models
from django.utils.translation import gettext as _

from common.models.mixins import TitleModelMixin
from common.models.base import BaseImageModel

from market.services.items import MarketItemParser

from . import validators


class Item(TitleModelMixin, BaseImageModel):
    title = models.CharField(verbose_name=_("Item title"),
                             max_length=100,
                             blank=True)
    image_path = models.URLField(verbose_name="Item image path",
                                 blank=True)
    price = models.FloatField(verbose_name="Price of item",
                              validators=[
                                  validators.MAX_ITEM_PRICE_VALIDATOR,
                                  validators.MIN_ITEM_PRICE_VALIDATOR
                              ],
                              blank=True)

    market_link = models.URLField(verbose_name="URL of this products on "
                                               "rust.rm",
                                  blank=False,
                                  default="unknown")

    class Meta:
        db_table = "items_items"

    def __init__(self, *args,
                 market_parser: MarketItemParser = MarketItemParser(),
                 **kwargs):
        self._market_parser = market_parser

        super().__init__(*args, **kwargs)

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

    def _get_image(self) -> models.URLField:
        return self.image_path
