from rest_framework import serializers

from .site import SiteFundsSerializer


class UserFundsStateSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    user_advantage = serializers.FloatField()


class UpgradeRequestSerializer(serializers.Serializer):
    granted_funds = serializers.IntegerField(allow_null=True, default=0)
    receive_funds = serializers.IntegerField(allow_null=True)
    user_funds = UserFundsStateSerializer(required=True)
    site_funds = SiteFundsSerializer(required=True)


class UpgradeRequestApiViewSerializer(serializers.Serializer):
    granted_funds = serializers.IntegerField(required=False,
                                             default=0,
                                             allow_null=True)
    granted_item_id = serializers.IntegerField(required=False,
                                               default=0,
                                               allow_null=True)

    receive_item_id = serializers.IntegerField(required=True)

    def validate(self, data: dict) -> dict:
        if (not (data.get("granted_funds") or data.get("granted_item_id"))) or (
            data.get("granted_funds") and data.get("granted_item_id")
        ):
            print("INVALID UPGRATE", data)
            raise serializers.ValidationError("Not correct upgrade values")

        return data
