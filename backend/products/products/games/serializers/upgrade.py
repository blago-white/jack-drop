from rest_framework import serializers

from .site import SiteFundsSerializer


class UserFundsStateSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    advantage = serializers.FloatField()

class UpgradeRequestSerializer(serializers.Serializer):
    granted_funds = serializers.IntegerField(allow_null=True, default=0)
    receive_funds = serializers.IntegerField(allow_null=True)
    user_funds = UserFundsStateSerializer(required=True)
    site_funds = SiteFundsSerializer(required=True)


class UpgradeRequestApiViewSerializer(serializers.Serializer):
    granted_funds = serializers.IntegerField(allow_null=True, default=0)
    granted_item_id = serializers.IntegerField(allow_null=True, default=0)

    receive_item_id = serializers.IntegerField(required=True)

    def validate(self, data: dict) -> dict:
        if ((not (data['granted_item_id'] or data['granted_funds'])) or
                (data['granted_item_id'] and data['granted_funds'])):
            raise serializers.ValidationError("Not correct upgrade values")

        return data
