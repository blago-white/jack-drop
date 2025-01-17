from django.core.exceptions import ValidationError
from django.db import models


class WithdrawedItem(models.Model):
    market_link = models.URLField()
    owner_trade_link = models.CharField()
    owner_id = models.IntegerField()
    success = models.BooleanField(default=False)


class Withdraw(models.Model):
    items = models.ManyToManyField(to=WithdrawedItem, null=True)
    date = models.DateTimeField(auto_now=True, editable=False)
    success = models.BooleanField(default=False)


class BotBalanceReplenish(models.Model):
    amount = models.FloatField()
    date = models.DateTimeField(auto_now=True, editable=False)


class ApiKey(models.Model):
    key = models.CharField(verbose_name="Api Key of market", max_length=1000)
    active = models.BooleanField(verbose_name="Can site use this key?",
                                 default=True)

    def __str__(self):
        return self.key

    def clean(self):
        if ApiKey.objects.all().filter(active=True).count() > 1:
            raise ValidationError("There should be only 1 active api key")


class Config(models.Model):
    withdraw_interval_seconds = models.IntegerField()
    withdraw_callback_url = models.CharField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and Config.objects.all().exists():
            raise ValidationError("Can add only one instance")

        return super().save(*args, **kwargs)
