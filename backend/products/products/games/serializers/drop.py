from rest_framework import serializers

from .users import UserAdvantageSerializer


class DropItemGameApiViewSerializer(serializers.Serializer):
    pass


class DropItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    rate = serializers.FloatField(min_value=0, max_value=100)
    price = serializers.FloatField(min_value=0)


class FundsState(serializers.Serializer):
    user_advantage = serializers.FloatField()
    site_active_funds_per_hour = serializers.FloatField(
        min_value=0
    )


class DropCaseRequestSerializer(serializers.Serializer):
    case_id = serializers.IntegerField(min_value=0)
    items = DropItemSerializer(many=True, required=True)
    funds = FundsState(required=True)
    price = serializers.IntegerField(min_value=0)
