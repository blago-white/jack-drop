from rest_framework import serializers

from .models import ClientBalance


class ClientBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientBalance
        fields = "__all__"
        read_only_fields = ["id"]


class UpdateClientBalanceSerializer(serializers.Serializer):
    delta_amount = serializers.FloatField(required=True)
