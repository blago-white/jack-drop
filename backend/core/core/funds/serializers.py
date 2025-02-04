from rest_framework import serializers


class UpdateDinamicSiteProfitSerializer(serializers.Serializer):
    delta_amount = serializers.FloatField()
    for_cases = serializers.BooleanField(default=False)
