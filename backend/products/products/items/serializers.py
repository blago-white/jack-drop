from rest_framework import serializers

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
