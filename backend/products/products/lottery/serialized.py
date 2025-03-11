from rest_framework import serializers

from items.serializers import ItemSerializer

from .models.lottery import LotteryEvent


class _LotteryPrizeSerializer(serializers.Serializer):
    winner_id = serializers.IntegerField(min_value=0)
    prize_item_id = serializers.IntegerField(min_value=0)


class LotteryResultsUsersEndpointSerializer(serializers.Serializer):
    prizes = _LotteryPrizeSerializer(required=True, many=True)


class LotteryDataSerializer(serializers.ModelSerializer):
    prize_secondary = ItemSerializer(required=True)
    prize_main = ItemSerializer(required=True)

    class Meta:
        model = LotteryEvent
        exclude = [
            "start_after",
            "winner_main",
            "winner_secondary",
            "is_dummy"
        ]
