from rest_framework import serializers


class TransactionCreationPubllicSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=500)


class TransactionCreationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_login = serializers.CharField(max_length=200)
    amount = serializers.FloatField(min_value=500)
    promocode = serializers.CharField(max_length=16,
                                      allow_null=True,
                                      allow_blank=True)


class SkinifyTransactionCreationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    steam_id = serializers.IntegerField(allow_null=True)
    trade_link = serializers.CharField(allow_null=True,
                                       allow_blank=True)
    promocode = serializers.CharField(max_length=16,
                                      allow_null=True,
                                      allow_blank=True)
