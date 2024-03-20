from django.db import models

from . import validators


class CaseItem(models.Model):
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
