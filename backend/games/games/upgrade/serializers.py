from rest_framework import serializers

from common.serializers import UserFundsStateSerializer, SiteFundsSerializer


class UpgradeRequestSerializer(serializers.Serializer):
    granted_funds = serializers.IntegerField(allow_null=True, default=0)
    receive_funds = serializers.IntegerField(allow_null=True)
    user_funds = UserFundsStateSerializer(required=True)
    site_funds = SiteFundsSerializer(required=True)
