from rest_framework.serializers import ModelSerializer, Serializer, FloatField
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Client
from accounts.services.users import UsersService


class ReadOnlyModelSerializer(ModelSerializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class PrivateClientSerializer(ReadOnlyModelSerializer):
    displayed_balance = serializers.FloatField(allow_null=True, default=0)
    user_advantage = serializers.FloatField(source="advantage.value")
    has_deposits = serializers.BooleanField(allow_null=True)

    class Meta:
        model = Client
        fields = ["id", "username", "steam_id", "avatar", "trade_link", "user_advantage", "displayed_balance", "has_deposits"]
        read_only_fields = ["id"]


class UpdateAdvantageSerializer(Serializer):
    delta_amount = FloatField()


class PublicClientSerializer(ReadOnlyModelSerializer):
    balance = serializers.FloatField(allow_null=True,
                                     default=0,
                                     source="displayed_balance")
    lottery_wins_list = serializers.ListField(default=[],
                                              required=False,
                                              allow_null=True,
                                              allow_empty=True)

    is_blogger = serializers.BooleanField(allow_null=False,
                                          default=False)

    class Meta:
        model = Client
        fields = ["id", "username", "trade_link", "avatar", "balance", "lottery_wins_list", "is_blogger"]
        read_only_fields = ["__all__"]


class TokenObtainPairWithoutPasswordSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        attrs.update({'password': ''})
        return super(TokenObtainPairWithoutPasswordSerializer, self).validate(attrs)


class _LotteryPrizeSerializer(serializers.Serializer):
    winner_id = serializers.IntegerField(min_value=0)
    prize_item_id = serializers.IntegerField(min_value=0)


class LotteryResultsSerializer(serializers.Serializer):
    prizes = _LotteryPrizeSerializer(required=True, many=True)
