from django.db.models.signals import post_save
from django.dispatch import receiver

from .client import ClientDeposit
from referrals.services.referral import ReferralService


def update_referral_level(sender, instance, **kwargs):
    ReferralService(
        deposit_model=instance.__class__
    ).update_referral_level(referr_id=instance.user.referral.first().referr)


post_save.connect(update_referral_level,
                  sender=ClientDeposit,
                  dispatch_uid="update_referral_level")

