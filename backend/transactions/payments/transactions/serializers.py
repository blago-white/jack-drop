from rest_framework import serializers


class TransactionCreationPubllicSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=500)


class TransactionCreationSerializer(serializers.Serializer):
    user_login = serializers.IntegerField()
    amount = serializers.FloatField(min_value=500)
