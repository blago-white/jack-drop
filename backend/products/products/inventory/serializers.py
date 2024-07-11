from rest_framework.serializers import ModelSerializer

from items.serializers import ItemSerializer
from .models import InventoryItem


class InventoryItemSerializer(ModelSerializer):
    item = ItemSerializer(required=True)

    class Meta:
        model = InventoryItem
        fields = ["id", "item"]
        read_only_fields = ["id", "item"]
