from rest_framework import serializers

from ..models.items import CaseItem
from .case import CaseSerializer


class CaseItemPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseItem
        fields = "__all__"
        read_only_fields = [
            "chance",
            "id"
        ]


class CaseWithItemsPrivateSerializer(serializers.Serializer):
    case = CaseSerializer(read_only=True)
    items = CaseItemPrivateSerializer(many=True, read_only=True)
