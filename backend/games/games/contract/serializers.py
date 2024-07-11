from rest_framework import serializers

from .models import Contract


class ShiftedContractAmountSerializer(serializers.Serializer):
    granted_amount = serializers.FloatField(min_value=0)


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"
        read_only_fields = ["pk"]
