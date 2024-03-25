from django.db import models
from django.contrib.auth.models import AbstractUser
from .config import MAX_PROMOCODE_LENGTH


class Client(AbstractUser):
    promocode = models.CharField(max_length=MAX_PROMOCODE_LENGTH,
                                 null=True,
                                 blank=True)
