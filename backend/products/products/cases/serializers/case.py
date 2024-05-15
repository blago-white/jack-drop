from rest_framework import serializers

from ..models.cases import Case


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        exclude = ["items"]
