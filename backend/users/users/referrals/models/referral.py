from hashlib import sha256

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from ..config import REFERR_LINK_MAX_LENGTH


class Referral(models.Model):
    user = models.OneToOneField(to=get_user_model(),
                                on_delete=models.CASCADE,
                                related_name="referral",
                                primary_key=True)

    referr = models.ForeignKey(to="self",
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    benefit_percent = models.IntegerField(blank=True, default=15)

    referr_link = models.CharField(max_length=REFERR_LINK_MAX_LENGTH,
                                   null=False,
                                   blank=True,
                                   unique=True)

    is_blogger = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f"{self.user} | {self.benefit_percent}%"

    def save(
            self, *args, **kwargs
    ):
        self.referr_link = sha256(self.user.username.encode(
            "utf-8"
        )).hexdigest()[:REFERR_LINK_MAX_LENGTH]

        self.benefit_percent = 20 if self.is_blogger else 15

        return super().save(*args, **kwargs)
