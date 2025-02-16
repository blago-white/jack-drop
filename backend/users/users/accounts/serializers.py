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

    class Meta:
        model = Client
        fields = ["id", "username", "avatar", "trade_link", "user_advantage", "displayed_balance"]
        read_only_fields = ["id"]


class UpdateAdvantageSerializer(Serializer):
    delta_amount = FloatField()


class PublicClientSerializer(ReadOnlyModelSerializer):
    balance = serializers.FloatField(allow_null=True,
                                     default=0,
                                     source="displayed_balance")

    is_blogger = serializers.BooleanField(allow_null=False,
                                          default=False)

    class Meta:
        model = Client
        fields = ["id", "username", "trade_link", "avatar", "balance", "is_blogger"]
        read_only_fields = ["__all__"]


class TokenObtainPairWithoutPasswordSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        attrs.update({'password': ''})
        return super(TokenObtainPairWithoutPasswordSerializer, self).validate(attrs)
