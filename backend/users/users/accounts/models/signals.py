from django.db.models.signals import post_save

from .client import Client
from referrals.services.referral import ReferralService
from balances.serivces.balance import ClientBalanceService


def create_referral(sender, instance, **kwargs) -> None:
    if not ReferralService(deposit_model=instance.__class__).user_exists(
        user_id=instance.pk
    ):
        ReferralService(
            deposit_model=instance.__class__
        ).create(
            user_id=instance.pk,
        )


def create_balance(sender, instance, **kwargs) -> None:
    if not ClientBalanceService().get_balance(
        client_id=instance.pk
    ):
        ClientBalanceService().create(
            client_id=instance.pk,
        )


post_save.connect(create_referral,
                  sender=Client,
                  dispatch_uid="create_referral")

post_save.connect(create_balance,
                  sender=Client,
                  dispatch_uid="create_balance")
