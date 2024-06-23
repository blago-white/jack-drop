from rest_framework import serializers

from items.serializers import ItemSerializer
from ..models.items import CaseItem
from .case import CaseSerializer


# class CaseItemPrivateSerializer(serializers.ModelSerializer):
#     items = ItemSerializer(required=True)
#
#     class Meta:
#         model = CaseItem
#         fields = "__all__"
#         read_only_fields = [
#             "rate",
#             "id"
#         ]


class CaseWithItemsPrivateSerializer(serializers.Serializer):
    case = CaseSerializer(read_only=True)
    items = ItemSerializer(many=True, read_only=True)
