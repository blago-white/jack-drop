from django.db import models

from accounts.models.client import Client


class ClientBalance(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    real_balance = models.FloatField(blank=True, default=0)
    displayed_balance = models.FloatField(blank=True, default=0)
