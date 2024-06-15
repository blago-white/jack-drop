from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe, escape

from common.models.base import BaseImageModel
from . import validators


class CaseItem(BaseImageModel):
    item = models.ForeignKey(verbose_name="Item",
                             to="items.Item",
                             on_delete=models.CASCADE)
    case = models.ForeignKey(verbose_name="Case of item",
                             to="cases.Case",
                             on_delete=models.CASCADE)
    rate = models.FloatField(verbose_name="Chance of item drop",
                             validators=[
                                 validators.MAX_CHANCE_VALUE_VALIDATOR,
                                 validators.MIN_CHANCE_VALUE_VALIDATOR
                             ],
                             blank=True,
                             default=0)
    can_drop = models.BooleanField(verbose_name="Can drop this item?",
                                   default=True)
    view = models.BooleanField(verbose_name="Can view this item?",
                               default=True)

    class Meta:
        db_table = "cases_case_items"
        unique_together = ["case", "item"]

    def __str__(self):
        return f"{self.item} in {self.case}"

    def clean(self):
        if self.can_drop and not self.view:
            raise ValidationError(
                "The item is hidden, but it can fall out, it is forbidden")

    def _get_image(self) -> models.URLField:
        return self.item.image_path

    def _get_case_image(self) -> models.URLField:
        return self.case.image_path

    def preview_case(self):
        return mark_safe(
            f"<img src=\"{escape(self._get_case_image())}\" style=\"width: 50px;\"/>"
        )
