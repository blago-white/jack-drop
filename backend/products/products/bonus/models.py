from django.db import models

from cases.models.cases import Case


class BonusBuyLevels(models.IntegerChoices):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


class CaseDiscount(models.Model):
    case = models.ForeignKey(to="cases.Case", on_delete=models.CASCADE)
    user_id = models.IntegerField()
    discount = models.IntegerField(verbose_name="Discount in percent [0-100]")

    def __str__(self):
        return f"{self.discount} | {self.user_id}"


class UserBonusBuyProfile(models.Model):
    user_id = models.IntegerField(primary_key=True)
    points = models.IntegerField(default=0, blank=True)
    level = models.ForeignKey("bonus.BonusBuyLevel",
                              on_delete=models.SET_DEFAULT,
                              default=1)
    active_free_cases = models.ManyToManyField(to="cases.Case",
                                               blank=True,
                                               editable=True)
    cases_discounts = models.ManyToManyField(to=CaseDiscount,
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


class FreeCase(models.Model):
    target_deposit_amount = models.FloatField()
    case = models.ForeignKey(to=Case, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.case} | {self.target_deposit_amount}"


class UsedDeposit(models.Model):
    deposit_id = models.BigIntegerField(primary_key=True)

    def __str__(self):
        return f"Deposit №{self.deposit_id}"
