import datetime

from django.db import models
from django.core.exceptions import ValidationError


def get_now_unix_time():
    return datetime.datetime.now().replace(tzinfo=None).timestamp()


class WinningTypes(models.TextChoices):
    PROMOCODE = "P", "Promocode for replenishment"
    CONTRACT = "C", "Free skin for contractr"
    FREE_SKIN = "F", "Free skin"
    CASE_DISCOUNT = "D", "Discount for case"
    UPGRADE = "U", "Skin for upgrade"


class FortuneWheelWinning(models.Model):
    user_id = models.IntegerField()

    site_funds_diff = models.FloatField()
    user_funds_diff = models.FloatField()

    winning_type = models.CharField(choices=WinningTypes.choices)
    win_time = models.DateTimeField(blank=True, auto_now=True)

    def __str__(self):
        return f"Winning {self.get_winning_type_display()}"


class FortuneWheelOpening(models.Model):
    user_id = models.IntegerField()
    result = models.JSONField(verbose_name="Result of game in JSON",
                              blank=True,
                              null=True)
    date = models.IntegerField(editable=False,
                               blank=True,
                               default=get_now_unix_time)

    class Meta:
        ordering = ["-date"]


class FortuneWheelPromocode(models.Model):
    promocode = models.CharField(max_length=8, primary_key=True)
    count_usages = models.IntegerField(
        default=1,
        blank=True
    )
    for_user = models.IntegerField(null=True, blank=True)


class FortuneWheelTimeout(models.Model):
    timeout = models.IntegerField(
        verbose_name="Unix datetime timeout between games"
    )

    def save(
            self, force_insert=False, force_update=False, using=None,
            update_fields=None
    ):
        if not self.pk and FortuneWheelTimeout.objects.all().count():
            raise ValidationError("Can add only one timeout")

        return super().save(force_insert=force_insert,
                            force_update=force_update,
                            update_fields=update_fields,
                            using=using)
