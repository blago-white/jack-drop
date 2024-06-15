from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from accounts.models import Client, ClientDeposit
from accounts.services.users import UsersService


class ReadOnlyModelSerializer(ModelSerializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class ClientSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "username", "promocode"]
        read_only_fields = ["id"]


class ClientDepositSerializer(ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UsersService().get_all()
    )

    class Meta:
        fields = ["user_id", "amount", "datetime"]
        read_only_fields = ["datetime"]
        model = ClientDeposit
