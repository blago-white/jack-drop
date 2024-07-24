from rest_framework import serializers

from accounts.services.users import UsersService

from .config import REFERR_LINK_MAX_LENGTH
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
        queryset=UsersService().get_all()
    )

    referr_link = serializers.CharField(max_length=REFERR_LINK_MAX_LENGTH)

    is_blogger = serializers.BooleanField(allow_null=True, default=False)

    benefit_percent = serializers.IntegerField(allow_null=True, default=15)


class ReferralLinkSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    referr_link = serializers.CharField(max_length=REFERR_LINK_MAX_LENGTH)
    is_valid = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        read_only_fields = ["is_valid", "user_id"]
