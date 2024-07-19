from rest_framework import serializers

from .models import UserBonusBuyProfile, BonusBuyLevel


class BonusBuyLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusBuyLevel
        fields = "__all__"


class BonusBuyProfileSerializer(serializers.ModelSerializer):
    level = BonusBuyLevelSerializer()
    can_withdraw_case = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = UserBonusBuyProfile
        fields = "__all__"
