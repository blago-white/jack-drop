from django.db import models


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
