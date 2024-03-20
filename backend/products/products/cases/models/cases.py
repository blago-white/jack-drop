from django.db import models

from common.models.mixins import TitleModelMixin
from items.models.models import Item
from cases.config import CASE_TITLE_MAX_LEN

from .items import CaseItem


class Case(TitleModelMixin, models.Model):
    items = models.ManyToManyField(verbose_name="Case Items",
                                   to=Item,
                                   through=CaseItem)
    title = models.CharField(verbose_name="Title of the case",
                             max_length=CASE_TITLE_MAX_LEN)

    class Meta:
        db_table = "cases_cases"
