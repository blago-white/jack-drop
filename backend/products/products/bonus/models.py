from django.db import models


class BonusBuyLevels(models.IntegerChoices):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


class UserBonusBuyProfile(models.Model):
    user_id = models.IntegerField(primary_key=True)
    points = models.IntegerField(default=0, blank=True)
    level = models.ForeignKey("bonus.BonusBuyLevel",
                              on_delete=models.SET_DEFAULT,
                              default=1)
    active_free_cases = models.ManyToManyField(to="cases.Case",
                                               null=True,
                                               blank=True,
                                               editable=True)
    withdraw_current = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f"Level {self.user_id} [{self.level.level}:{self.points}xp]"


class BonusBuyLevel(models.Model):
    level = models.IntegerField(choices=BonusBuyLevels.choices,
                                default=BonusBuyLevels.FIRST,
                                primary_key=True)
    free_case = models.ForeignKey(to="cases.Case",
                                  on_delete=models.SET_NULL,
                                  null=True)
    target = models.IntegerField()

    class Meta:
        ordering = ["level"]

    def __str__(self):
        return f"Level {self.level} (req. {self.target})"
