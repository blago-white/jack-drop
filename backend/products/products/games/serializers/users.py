from rest_framework import serializers


class GetUserInfoEndpointSerializer(serializers.Serializer):
    pass


class UserAdvantageSerializer(serializers.Serializer):
    user_advantage = serializers.FloatField()


class UserAdvantageIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    user_advantage = serializers.FloatField()


class DetailedUserFundsSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    user_advantage = serializers.FloatField()
    displayed_balance = serializers.FloatField(required=True, min_value=0)
    trade_link = serializers.CharField()
    has_deposits = serializers.BooleanField(default=False)
