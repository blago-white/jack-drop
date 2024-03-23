from django.db import models

from common.models.base import BaseModel

from . import validators


class CaseItem(BaseModel):
    item = models.ForeignKey(verbose_name="Item",
                             to="items.Item",
                             on_delete=models.CASCADE)
    case = models.ForeignKey(verbose_name="Case of item",
                             to="cases.Case",
                             on_delete=models.CASCADE)
    chance = models.FloatField(verbose_name="Chance of item drop",
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

    def __str__(self):
        return f"{self.item} in {self.case}"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # TODO: Updating the chances of falling out for all items
        #  from the case when adding a new one

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            update_fields=force_update,
            using=using,
        )
