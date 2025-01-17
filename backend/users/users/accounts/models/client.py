from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class Client(AbstractUser):
    steam_id = models.PositiveBigIntegerField(unique=True, default=0)

    advantage = models.FloatField(default=-100)

    trade_link = models.CharField(null=True, blank=True, max_length=200)

    avatar = models.CharField(
        default="/core/static/img/account-avatar.png",
        max_length=1000,
        blank=True
    )
