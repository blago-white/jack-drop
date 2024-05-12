from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .utils import ReferralLevels


class ReferralBenefit(models.Model):
    level = models.IntegerField(choices=ReferralLevels.choices)
    discount_per_referral = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    required_deposits = models.IntegerField(
        "Sum of deps for up to this level"
    )

    def __str__(self):
        return f"Level: {self.level} ({self.discount_per_referral}%)"


class Referral(models.Model):
    user = models.ForeignKey(to=get_user_model(),
                             on_delete=models.CASCADE,
                             related_name="referral",
                             primary_key=True,
                             unique=True)

    referr = models.ForeignKey(to=get_user_model(),
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name="referr")

    benefit = models.ForeignKey(to=ReferralBenefit,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)

    def __str__(self):
        return f"{self.user} {self.benefit}"

    def clean(self):
        if self.referr and not self.benefit:
            raise ValidationError("Cannot set reffer without benefit")
