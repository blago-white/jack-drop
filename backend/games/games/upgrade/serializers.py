from rest_framework import serializers


class UserFundsStateSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    advantage = serializers.FloatField()


class SiteFundsSerializer(serializers.Serializer):
    site_active_funds_per_hour = serializers.FloatField(min_value=0)


class UpgradeRequestSerializer(serializers.Serializer):
    granted_funds = serializers.IntegerField(allow_null=True, default=0)
    receive_funds = serializers.IntegerField(allow_null=True)
    user_funds = UserFundsStateSerializer(required=True)
    site_funds = SiteFundsSerializer(required=True)
