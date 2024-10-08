from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError

from accounts.models.client import Client

from .config import MAX_PROMOCODE_LENGTH


class Promocode(models.Model):
    code = models.CharField(max_length=MAX_PROMOCODE_LENGTH,
                            unique=True,
                            verbose_name="Promo code")
    discount = models.IntegerField(verbose_name="Discount percent",
                                   validators=[
                                       MinValueValidator(0),
                                       MaxValueValidator(100)
                                   ])
    usages = models.IntegerField(verbose_name="Count usages, -1 = infinite",
                                 default=-1)

    class Meta:
        ordering = ["-discount"]

    def __str__(self):
        return f"{self.code[:10]} [{self.discount}%]"

    def save(self, *args, **kwargs):
        if -1 > self.usages:
            raise ValidationError("Not correct usages count!")

        return super().save(*args, **kwargs)


class PromocodeActivation(models.Model):
    client = models.ForeignKey(to=Client,
                               null=True,
                               on_delete=models.SET_NULL)

    promocode = models.ForeignKey(to=Promocode,
                                  null=True,
                                  on_delete=models.SET_NULL)

    datetime = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.client.username} | {self.promocode}"
