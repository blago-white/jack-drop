from django.db import models

from common.models.mixins import TitleModelMixin
from categories.config import MAX_CATEGORY_TITLE_NAME


class CasesCategory(TitleModelMixin, models.Model):
    title = models.CharField(verbose_name="Title of the category",
                             max_length=MAX_CATEGORY_TITLE_NAME)
    cases = models.ForeignKey(verbose_name="Cases of the category",
                              to="cases.Case",
                              on_delete=models.CASCADE,
                              null=True)

    class Meta:
        db_table = "categories_categories"
        verbose_name_plural = "Cases Categories"
        verbose_name = "Case Category"
