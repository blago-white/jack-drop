from rest_framework import serializers

from .models import WinningTypes
from common.serializers import SiteFundsSerializer, UserFundsStateSerializer


class PrizeRequestSerializer(serializers.Serializer):
    site_funds = SiteFundsSerializer(required=True)
    user_funds = UserFundsStateSerializer()
    type = serializers.CharField()
    additional_data = serializers.JSONField(allow_null=True)


class PrizeSerializer(serializers.Serializer):
    prize = serializers.JSONField(allow_null=False)
    user_funds_diff = serializers.FloatField()
    site_funds_diff = serializers.FloatField()
    type = serializers.ChoiceField(
        choices=WinningTypes.choices
    )


class PrizeTypeRequestSerializer(serializers.Serializer):
    site_funds = SiteFundsSerializer()
    user_funds = UserFundsStateSerializer()
    min_item_price = serializers.FloatField()


class PrizeTypeSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=WinningTypes.choices
    )


class FortuneWheelTimeoutSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=0)


class FortuneWheelTimeoutValueSerializer(serializers.Serializer):
    timeout = serializers.IntegerField(min_value=0)


class UsePromocodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=0)
    promocode = serializers.CharField(max_length=8)
