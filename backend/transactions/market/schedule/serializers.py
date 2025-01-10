from rest_framework import serializers


class WithdrawItemSerializer(serializers.Serializer):
    inventory_item_id = serializers.IntegerField(min_value=0)
    inventory_item_hash_name = serializers.CharField()
    item_market_link = serializers.URLField()
    owner_trade_link = serializers.CharField()
    item_price = serializers.FloatField(min_value=0)
