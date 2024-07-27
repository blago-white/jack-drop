from rest_framework import serializers

from accounts.services.users import UsersService

from .models import ClientBalance, ClientDeposit


class ClientBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientBalance
        fields = "__all__"
        read_only_fields = ["id"]


class UpdateClientBalanceSerializer(serializers.Serializer):
    delta_amount = serializers.FloatField(required=True)


class ClientDepositSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UsersService().get_all(),
        required=False
    )

    amount = serializers.FloatField(min_value=500)

    class Meta:
        fields = ["id", "user_id", "amount", "datetime"]
        read_only_fields = ["datetime"]
        model = ClientDeposit
