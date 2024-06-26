from django.db.models.signals import post_save

from .client import ClientDeposit, Client
from referrals.services.referral import ReferralService
from balances.models import ClientBalance


def update_referral_level(sender, instance, **kwargs) -> None:
    ReferralService(
        deposit_model=instance.__class__
    ).update_referral_level(
        referr_id=instance.user.referral.first().referr
    )


def create_referral(sender, instance, **kwargs) -> None:
    ReferralService(
        deposit_model=instance.__class__
    ).create(
        user_id=instance.pk,
    )


def create_balance(sender, instance, **kwargs) -> None:
    ReferralService(
        deposit_model=instance.__class__
    ).create(
        user_id=instance.pk,
    )


post_save.connect(update_referral_level,
                  sender=ClientDeposit,
                  dispatch_uid="update_referral_level")

post_save.connect(create_referral,
                  sender=Client,
                  dispatch_uid="create_referral")
