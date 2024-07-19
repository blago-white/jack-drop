from django.db import models


class BonusBuyLevels(models.IntegerChoices):
    FIRST = 1, "5_000"
    SECOND = 2, "10_000"
    THIRD = 3, "25_000"
    FOUR = 4, "50_000"
    FIVE = 5, "140_000"
    SIX = 6, "220_000"
    SEVEN = 7, "400_000"
    EIGHT = 8, "1_000_000"


class UserBonusBuyProfile(models.Model):
    user_id = models.IntegerField(primary_key=True)
    points = models.IntegerField(default=0, blank=True)
    level = models.IntegerField(choices=BonusBuyLevels.choices,
                                default=BonusBuyLevels.FIRST,
                                blank=True)
    active_free_cases = models.ForeignKey(to="cases.Case",
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True)
