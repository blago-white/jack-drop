from django.db import models

from common.models.mixins import TitleModelMixin
from common.models.base import BaseModel

from items.models.models import Item
from cases.config import CASE_TITLE_MAX_LEN

from .items import CaseItem


class Case(TitleModelMixin, BaseModel):
    items = models.ManyToManyField(verbose_name="Case Items",
                                   to=Item,
                                   through=CaseItem)
    title = models.CharField(verbose_name="Title of the case",
                             max_length=CASE_TITLE_MAX_LEN)

    category = models.ForeignKey(verbose_name="Name of category",
                                 to="categories.CasesCategory",
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    class Meta:
        db_table = "cases_cases"
