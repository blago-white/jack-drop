from rest_framework import serializers

from accounts.models import Client

from .services.referral import ReferralService
from .models.utils import ReferralLevels


class ClaculatedDiscount(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        count_referrals = serializer_field.parent.initial_data.get("referrals")

        return ReferralService().get_discount(
            count_referrals=count_referrals
        )


class ReferralStatusSerializer(serializers.Serializer):
    referr = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all()
    )

    referrals = serializers.IntegerField(allow_null=True,
                                         initial=0,
                                         default=0)

    level = serializers.ChoiceField(
        choices=referralLevels.choices
    )

    discount = serializers.IntegerField(allow_null=True,
                                        initial=0,
                                        default=ClaculatedDiscount())
