from rest_framework import serializers


class ProductsDepositWebhookSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=0)
    deposit_id = serializers.IntegerField(min_value=0)
    amount = serializers.FloatField(min_value=500)

