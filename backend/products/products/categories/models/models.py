from django.db import models

from common.models.mixins import TitleModelMixin
from common.models.base import BaseModel

from categories.config import MAX_CATEGORY_TITLE_NAME


class CasesCategory(TitleModelMixin, BaseModel):
    slug = models.SlugField(primary_key=True, default="test")
    title = models.CharField(verbose_name="Title of the category",
                             max_length=MAX_CATEGORY_TITLE_NAME)

    class Meta:
        db_table = "categories_categories"
        verbose_name_plural = "Cases Categories"
        verbose_name = "Case Category"
