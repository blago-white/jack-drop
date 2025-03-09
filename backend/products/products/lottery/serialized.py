from rest_framework import serializers


class _LotteryPrizeSerializer(serializers.Serializer):
    winner_id = serializers.IntegerField(min_value=0)
    prize_item_id = serializers.IntegerField(min_value=0)


class LotteryResultsUsersEndpointSerializer(serializers.Serializer):
    prizes = _LotteryPrizeSerializer(required=True, many=True)
