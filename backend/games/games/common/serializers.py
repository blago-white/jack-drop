from rest_framework import serializers


class UserFundsStateSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    user_advantage = serializers.FloatField()


class SiteFundsSerializer(serializers.Serializer):
    site_active_funds_per_hour = serializers.FloatField(min_value=0)
