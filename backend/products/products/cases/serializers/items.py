from rest_framework import serializers

from ..models.items import CaseItem
from .case import CaseSerializer


class CaseItemSerializer(serializers.ModelSerializer):
    case = CaseSerializer()

    class Meta:
        model = CaseItem
        fields = "__all__"
        read_only_fields = [
            "chance",
            "id"
        ]
