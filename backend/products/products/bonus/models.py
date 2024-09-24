from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from cases.models.cases import Case
from items.models.models import Item


class BonusBuyLevels(models.IntegerChoices):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


class BonusTypes(models.TextChoices):
    CASE_DISCOUNT = "CD", "Case Discount"
    PROMOCODE = "PR", "Promo For Replenish"
    FREE_SKIN = "FR", "Free Skin"
    FREE_CONTRACT_SKIN = "CS", "Free Contract Skin"
    FREE_UPGRADE_SKIN = "US", "Free Upgrade Skin"
    FREE_CASE = "FC", "Free Case"


class BonusCase(models.Model):
    case = models.ForeignKey(to="cases.Case", on_delete=models.CASCADE)
    discount = models.IntegerField(verbose_name="Discount in percent [0-100]",
                                   validators=[
                                       MinValueValidator(0),
                                       MaxValueValidator(100)
                                   ], default=0, blank=True)
    is_free = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.case} | {self.discount}%"


class UserBonus(models.Model):
    user_id = models.IntegerField()
    bonus_type = models.CharField(choices=BonusTypes.choices)
    active = models.BooleanField(default=True, null=True)
    related_case = models.ForeignKey(to=BonusCase,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True)
    related_item = models.ForeignKey(to=Item,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True)
    related_promo = models.CharField(max_length=16,
                                     null=True,
                                     blank=True)
    date_receive = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.get_bonus_type_display()}| uid: {self.user_id}"


class UserBonusBuyProfile(models.Model):
    user_id = models.IntegerField(primary_key=True)
    points = models.IntegerField(default=0, blank=True)
    level = models.ForeignKey("bonus.BonusBuyLevel",
                              on_delete=models.SET_DEFAULT,
                              default=1)
    free_cases = models.ManyToManyField(to=Case, editable=True)

    def __str__(self):
        return f"Bonus Buy {self.user_id} [{self.level.level}:{self.points}xp]"


class BonusBuyLevel(models.Model):
    level = models.IntegerField(choices=BonusBuyLevels.choices,
                                default=BonusBuyLevels.FIRST,
                                primary_key=True)
    free_case = models.ForeignKey(verbose_name="Free case for level [!DO NOT ADD THE IDENTICAL CASES!]",
                                  to="cases.Case",
                                  on_delete=models.SET_NULL,
                                  null=True)
    target = models.IntegerField(verbose_name="Amount of points for level")

    class Meta:
        ordering = ["level"]

    def __str__(self):
        return f"Level {self.level} (req. {self.target})"


class FreeDepositCase(models.Model):
    target_deposit_amount = models.FloatField()
    case = models.ForeignKey(to=Case, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.case} | {self.target_deposit_amount}"


class UsedDeposit(models.Model):
    deposit_id = models.BigIntegerField(primary_key=True)

    def __str__(self):
        return f"Deposit №{self.deposit_id}"


class FakeCaseDiscount(models.Model):
    pass

    class Meta:
        db_table = "casediscount"
