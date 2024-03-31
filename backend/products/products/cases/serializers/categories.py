from rest_framework import serializers

from .case import CaseSerializer


class CasesByCategoriesSerializer(serializers.Serializer):
    category = serializers.CharField(read_only=True)
    cases = CaseSerializer(many=True, read_only=True)
