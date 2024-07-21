from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import CheckConstraint


class SingleInstanceModel(models.Model):
    class Meta:
        abstract = True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.__class__.objects.all().count() == 1 and not self.pk:
            raise ValidationError("Can add only one instance!")

        return super().save(force_insert, force_update, using, update_fields)


class FrozenSiteProfit(SingleInstanceModel):
    amount = models.FloatField("You can withdraw this funds")

    def __str__(self):
        return f"Frozen site profit now: {self.amount}"

    class Meta:
        verbose_name = "Frozen Profit"
        verbose_name_plural = "Frozen Profits"


class DinamicSiteProfit(SingleInstanceModel):
    amount = models.FloatField("DONT WITHDRAW THIS FUNDS")
    min_value = models.FloatField("Min value of site profit", default=0)
    time_update = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return f"Dinamic site profit now: {self.amount}"

    class Meta:
        verbose_name = "Dinamic Profit"
        verbose_name_plural = "Dinamic Profits"


class FreezeFundsPercent(SingleInstanceModel):
    percent = models.IntegerField("Percent of dinamic funds, wich convert to "
                                  "frozen funds")

    class Meta:
        constraints = [
            CheckConstraint(
                check=models.Q(percent__gte=0) | models.Q(percent__lte=100),
                name="percent_valid_value"
            )
        ]

    def __str__(self):
        return f"Percent: {self.percent}"
