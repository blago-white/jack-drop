from django.db import models
from django.utils.translation import gettext_lazy as _

from cases.config import CASE_TITLE_MAX_LEN
from common.models.base import BaseImageModel
from common.models.mixins import TitleModelMixin
from items.models.models import Item


class Case(TitleModelMixin, BaseImageModel):
    items = models.ManyToManyField(verbose_name=_("Case Items"),
                                   to=Item,
                                   through="cases.CaseItem")
    title = models.CharField(verbose_name=_("Title of the case"),
                             max_length=CASE_TITLE_MAX_LEN,
                             unique=True)

    category = models.ForeignKey(verbose_name=_("Name of category"),
                                 to="categories.CasesCategory",
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    image_path = models.URLField(verbose_name=_("Case image path"),
                                 blank=False,
                                 default="/",
                                 unique=True)

    price = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "cases_cases"

    def _get_image(self) -> models.URLField:
        return self.image_path
