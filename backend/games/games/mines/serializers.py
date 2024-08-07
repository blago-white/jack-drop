from rest_framework import serializers

from common.serializers import UserFundsStateSerializer, SiteFundsSerializer
from .models import MinesGame


class MinesGameInitSerializer(serializers.Serializer):
    count_mines = serializers.IntegerField(allow_null=False,
                                           required=True,
                                           min_value=1)

    user_funds = UserFundsStateSerializer()
    user_deposit = serializers.FloatField(min_value=1)

    site_funds = SiteFundsSerializer(required=True)


class MinesGameNextStepSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    site_funds = SiteFundsSerializer(required=True)


class FundsDifferenceSerializer(serializers.Serializer):
    user_funds_diff = serializers.FloatField()
    site_funds_diff = serializers.FloatField()
    game_ended = serializers.BooleanField(default=True, allow_null=True)


class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinesGame
        fields = "__all__"


class MinesGameResultSerializer(serializers.Serializer):
    funds_difference = FundsDifferenceSerializer()
    mines_game = GameResultSerializer()
