from rest_framework import serializers


class WithdrawItemSerializer(serializers.Serializer):
    inventory_item_id = serializers.IntegerField(min_value=0)
    inventory_item_hash_name = serializers.IntegerField(min_value=0)
    owner_trade_link = serializers.IntegerField(min_value=0)
    item_price = serializers.FloatField(min_value=0)
