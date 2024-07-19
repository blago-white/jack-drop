from rest_framework import serializers

from .models import UserBonusBuyProfile


class BonusBuyProfileSerializer(serializers.ModelSerializer):
    target = serializers.IntegerField(source="get_level_display")

    class Meta:
        model = UserBonusBuyProfile
        fields = "__all__"
