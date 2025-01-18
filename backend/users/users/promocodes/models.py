from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError

from accounts.models.client import Client

from .config import MAX_PROMOCODE_LENGTH


class Promocode(models.Model):
    code = models.CharField(max_length=MAX_PROMOCODE_LENGTH,
                            unique=True,
                            verbose_name="Promo code")
    blogger = models.OneToOneField(to="referrals.Referral",
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name="promocodes",
                                   related_query_name="promocodes")
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


class PromocodeActivation(models.Model):
    client = models.ForeignKey(to=Client,
                               null=True,
                               on_delete=models.SET_NULL)

    promocode = models.ForeignKey(to=Promocode,
                                  null=True,
                                  on_delete=models.SET_NULL)

    datetime = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        if self.client:
            return f"{self.client.username} | {self.promocode}"
        else:
            return f"<unknows_user> | {self.promocode}"
