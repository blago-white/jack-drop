from rest_framework import serializers

from cases.services.items import CaseItemsService
from .models.models import Item, ItemsSet
from .services.items import ItemService


class RawPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        try:
            return super().to_representation(value=value)
        except AttributeError:
            if self.pk_field is not None:
                return self.pk_field.to_representation(value)
            return value


class ItemPriceSerializer(serializers.Serializer):
    item_id = RawPrimaryKeyRelatedField(
        queryset=ItemService().get_all()
    )

    price = serializers.IntegerField(default=0)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
        read_only_fields = ["__all__"]


class ItemWithCaseItemSerializer(serializers.ModelSerializer):
    case_item_id = serializers.PrimaryKeyRelatedField(
        queryset=CaseItemsService().get_all()
    )
    winrate = serializers.RelatedField(
        source="rate",
        read_only=True
    )

    class Meta:
        model = Item
        fields = "__all__"
        read_only_fields = ["__all__"]


class ItemsSetSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = ItemsSet
        fields = "__all__"
