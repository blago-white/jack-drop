from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .utils import ReferralLevels


class Referral(models.Model):
    user_id = models.ForeignKey(to=get_user_model(),
                                on_delete=models.CASCADE)

    referr = models.ForeignKey(to=get_user_model(),
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    benefit = models.ForeignKey(to="referrals.ReferalBenefit",
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)

    def clean(self):
        if self.referr and not self.benefit:
            raise ValidationError("Cannot set reffer without benefit")


class ReferralBenefit(models.Model):
    level = models.IntegerField(choices=ReferralLevels.choices)
    discount_per_referral = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    require_referrals = models.IntegerField(
        "Count of referrals for up to this level"
    )
