from django.db import models

from accounts.models.client import Client


class ClientBalance(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    real_balance = models.FloatField(blank=True, default=0)
    displayed_balance = models.FloatField(blank=True, default=0)


class ClientDeposit(models.Model):
    user = models.ForeignKey(to="accounts.Client",
                             on_delete=models.CASCADE)

    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    amount = models.PositiveIntegerField()

    bonused = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Deposit {self.user}"

    class Meta:
        ordering = ["-datetime"]
