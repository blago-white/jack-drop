from django.db import models
from django.core.exceptions import ValidationError


class WithdrawedItem(models.Model):
    market_link = models.URLField()


class Withdraw(models.Model):
    items = models.ForeignKey(to=WithdrawedItem, on_delete=models.SET_NULL, null=True)

    date = models.DateTimeField(auto_now=True, editable=False)


class BotBalanceReplenish(models.Model):
    amount = models.FloatField()

    date = models.DateTimeField(auto_now=True, editable=False)


class Config(models.Model):
    withdraw_interval_seconds = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.pk and Config.objects.all().exists():
            raise ValidationError("Can add only one instance")

        return super().save(*args, **kwargs)
