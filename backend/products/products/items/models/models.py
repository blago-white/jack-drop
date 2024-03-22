from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import escape, mark_safe

from common.models.mixins import TitleModelMixin
from common.models.base import BaseModel

from items.services.items import MarketItemParser

from . import validators


class Item(TitleModelMixin, BaseModel):
    title = models.CharField(verbose_name="Item title",
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

    manage_manually = models.BooleanField(verbose_name="Edit this item data "
                                                       "manualy?",
                                          default=False,
                                          )

    class Meta:
        db_table = "items_items"

    def save(
            self, force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        if (not (self.title and self.image_path and self.price)
                and self.manage_manually is True):
            raise ValidationError("If you want to manage the item manually, "
                                  "fill in all the required fields")

        if self.manage_manually is False:
            self._update_fields()

        return super().save()

    def preview(self):
        return mark_safe(f'<img src="{escape(self.image_path)}"/>')

    def preview_short(self):
        return mark_safe(
            f"<img src=\"{escape(self.image_path)}\" style=\"width: 50px;\"/>"
        )

    def _update_fields(self) -> None:
        parser = MarketItemParser()

        item_info = parser.get_info(self.market_link)

        self.title = item_info.title
        self.image_path = item_info.image_path
        self.price = item_info.price
