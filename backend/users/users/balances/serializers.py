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

    amount = serializers.FloatField(min_value=499)

    promocode = serializers.CharField(max_length=16,
                                      allow_null=True,
                                      required=False)

    class Meta:
        fields = ["id", "user_id", "amount", "datetime", "promocode", "bonused"]
        read_only_fields = ["datetime", "bonused"]
        model = ClientDeposit
