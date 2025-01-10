from rest_framework import serializers

from items.serializers import ItemSerializer
from .models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(required=True)

    class Meta:
        model = InventoryItem
        fields = ["id", "item"]
        read_only_fields = ["id", "item"]


class ScheduledItemSerializer(serializers.Serializer):
    inventory_item_id = serializers.IntegerField(min_value=0)
    inventory_item_hash_name = serializers.CharField()
    item_market_link = serializers.URLField()
    owner_trade_link = serializers.CharField()
    item_price = serializers.FloatField(min_value=0)

