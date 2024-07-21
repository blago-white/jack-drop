from rest_framework import serializers

from ..models.cases import Case


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        read_only_fields = ["__all__"]
        fields = "__all__"
