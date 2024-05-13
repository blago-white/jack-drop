from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# from referrals.services.referral import ReferralService


class ClientDeposit(models.Model):
    user = models.ForeignKey(to="accounts.Client",
                             on_delete=models.CASCADE)

    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"Deposit {self.user}"

    class Meta:
        ordering = ["-datetime"]


class Client(AbstractUser):
    promocode = models.ForeignKey(to="promocodes.Promocode",
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True)

    def save(self, *args, **kwargs):
        # ReferralService(deposit_model=ClientDeposit).create(user_id=self.pk)

        return super().save(*args, **kwargs)
