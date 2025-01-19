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

    benefit_percent = models.IntegerField(blank=True, default=30)

    referr_link = models.CharField(max_length=REFERR_LINK_MAX_LENGTH,
                                   null=False,
                                   blank=True,
                                   unique=True)

    is_blogger = models.BooleanField(blank=True, default=False)

    referrals_loses_funds = models.FloatField(blank=True, default=0)

    def __str__(self):
        return f"{self.user} | {self.benefit_percent}%"

    @property
    def full_refer_link(self):
        return f"https://jackdrop.online/auth/&ref={self.referr_link}"

    def save(
            self, *args, **kwargs
    ):
        self.referr_link = sha256(self.user.username.encode(
            "utf-8"
        )).hexdigest()[:REFERR_LINK_MAX_LENGTH]

        return super().save(*args, **kwargs)
