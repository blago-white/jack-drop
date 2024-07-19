from rest_framework import serializers

from .models import UserBonusBuyProfile


class BonusBuyProfileSerializer(serializers.ModelSerializer):
    target = serializers.IntegerField(source="level.target")

    class Meta:
        model = UserBonusBuyProfile
        fields = "__all__"
