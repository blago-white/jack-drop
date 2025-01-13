from rest_framework import serializers


class TransactionCreationPubllicSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=500)


class TransactionCreationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_login = serializers.CharField(max_length=200)
    amount = serializers.FloatField(min_value=500)
