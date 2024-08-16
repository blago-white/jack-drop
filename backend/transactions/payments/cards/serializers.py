from rest_framework import serializers


class TransactionCreationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    payin = serializers.CharField()
    amount = serializers.FloatField(min_value=500)
