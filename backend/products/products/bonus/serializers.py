from rest_framework import serializers

from cases.serializers.case import CaseSerializer
from cases.config import CASE_TITLE_MAX_LEN

from items.config import ITEM_TITLE_MAX_LENGTH

from .models import UserBonusBuyProfile, BonusBuyLevel, UserBonus


class BonusBuyLevelSerializer(serializers.ModelSerializer):
    free_case = CaseSerializer()

    class Meta:
        model = BonusBuyLevel
        fields = "__all__"


class BonusBuyProfileSerializer(serializers.ModelSerializer):
    level = BonusBuyLevelSerializer()
    can_withdraw_case = serializers.BooleanField(required=False, default=False)
    free_cases = CaseSerializer(many=True)

    class Meta:
        model = UserBonusBuyProfile
        fields = "__all__"


class UserFreeCaseAddSerializer(serializers.Serializer):
    deposit_id = serializers.IntegerField(min_value=0)
    amount = serializers.FloatField(min_value=0)
    user_id = serializers.IntegerField(min_value=0)


class UserBonusesSerializer(serializers.ModelSerializer):
    case_title = serializers.CharField(
        max_length=CASE_TITLE_MAX_LEN,
        allow_blank=True,
        allow_null=True
    )
    case_discount = serializers.IntegerField(
        default=0,
        min_value=0,
        max_value=100,
        allow_blank=True,
    )
    case_is_free = serializers.BooleanField(default=False)
    item_title = serializers.CharField(
        max_length=ITEM_TITLE_MAX_LENGTH,
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = UserBonus

        fields = [
            "bonus_type",
            "case_title",
            "case_discount",
            "case_is_free",
            "item_title"
        ]
