from rest_framework import serializers

from inventory.services.inventory import InventoryService


class ShiftedContractAmountSerializer(serializers.Serializer):
    granted_amount = serializers.FloatField(min_value=0)


class CommitContractSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(max_value=1)
    granted_amount = serializers.FloatField()
    result_item = serializers.IntegerField()


class GrantedInventoryItemsSerializer(serializers.Serializer):
    granted_inventory_items = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=InventoryService().get_all()
        ),
        allow_null=False
    )
