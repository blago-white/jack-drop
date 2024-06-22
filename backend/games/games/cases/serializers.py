from rest_framework import serializers


class DropItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    rate = serializers.FloatField(min_value=0, max_value=100)
    price = serializers.FloatField(min_value=0)


class ResultFundsState(serializers.Serializer):
    user_funds_delta = serializers.FloatField()
    site_funds_delta = serializers.FloatField(
        min_value=0
    )


class FundsState(serializers.Serializer):
    user_funds = serializers.FloatField()
    site_active_funds = serializers.FloatField(
        min_value=0
    )


class DropCaseRequestSerializer(serializers.Serializer):
    case_id = serializers.IntegerField(min_value=0)
    items = DropItemSerializer(many=True, required=True)
    funds = FundsState(required=True)
    price = serializers.IntegerField(min_value=0)


class DropResultSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(min_value=0, read_only=True)
    funds = ResultFundsState(read_only=True)
