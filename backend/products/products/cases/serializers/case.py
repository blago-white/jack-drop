from rest_framework import serializers

from ..models.cases import Case
from ..models.items import CaseItem


class CaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseItem
        read_only_fields = "__all__"
        fields = "__all__"


class CaseSerializer(serializers.ModelSerializer):
    items = CaseItemSerializer(many=True, allow_null=True)

    class Meta:
        model = Case
        read_only_fields = "__all__"
        fields = "__all__"
