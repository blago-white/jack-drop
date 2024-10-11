from rest_framework import serializers

from cases.serializers.case import CaseSerializer
from .models import UserBonusBuyProfile, BonusBuyLevel


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
