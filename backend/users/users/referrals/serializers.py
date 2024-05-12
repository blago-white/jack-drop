from rest_framework import serializers

from accounts.models import Client
from .models.utils import ReferralLevels
from .services.referral import ReferralBenefitService


class ClaculatedDiscount(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        deposits_amount = serializer_field.parent.initial_data.get("deposits")

        return ReferralBenefitService().get_discount(
            deposits_amount=deposits_amount
        )


class ClaculatedLevel(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        deposits_amount = serializer_field.parent.initial_data.get("deposits")

        return ReferralBenefitService().get_level(
            required_deposits=deposits_amount
        ).level


class ReferralStatusSerializer(serializers.Serializer):
    referr_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all().values("pk")
    )

    deposits = serializers.IntegerField(allow_null=False,
                                        initial=0,
                                        default=0)

    level = serializers.ChoiceField(
        choices=ReferralLevels.choices,
        default=ClaculatedLevel()
    )

    personal_discount = serializers.IntegerField(allow_null=True,
                                                 initial=0,
                                                 default=ClaculatedDiscount())
