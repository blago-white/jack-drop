from rest_framework import serializers


class GetUserInfoEndpointSerializer(serializers.Serializer):
    pass


class UserAdvantageSerializer(serializers.Serializer):
    user_advantage = serializers.FloatField()


class UserFundsSerializer(serializers.Serializer):
    advantage = UserAdvantageSerializer(required=True)
    desplayed_balance = serializers.FloatField(required=True, default=0)
