from rest_framework import serializers


class GetUserInfoEndpointSerializer(serializers.Serializer):
    pass


class UserAdvantageSerializer(serializers.Serializer):
    user_advantage = serializers.FloatField()


class UserFundsSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, min_value=0)
    user_advantage = serializers.FloatField()
    displayed_balance = serializers.FloatField(required=True, min_value=0)
