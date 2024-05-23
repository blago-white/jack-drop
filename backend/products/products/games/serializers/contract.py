from rest_framework import serializers

from inventory.services.inventory import InventoryService


class ShiftedContractAmountSerializer(serializers.Serializer):
    granted_amount = serializers.FloatField(min_value=0)


class CommitContractSerializer(serializers.Serializer):
    granted_amount = serializers.FloatField()
    result_item = serializers.IntegerField()


class GrantedInventoryItemSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryService().get_all()
    )


class GrantedInventoryItemsSerializer(serializers.Serializer):
    granted_inventory_items = serializers.ListField(
        child=GrantedInventoryItemSerializer(),
        allow_null=False
    )
