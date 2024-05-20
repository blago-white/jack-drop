from rest_framework import serializers

from .services.items import ItemService


class ItemPriceSerializer(serializers.Serializer):
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=ItemService().get_all()
    )

    price = serializers.IntegerField(default=0)
