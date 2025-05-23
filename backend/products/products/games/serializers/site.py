from rest_framework import serializers


class SiteFundsSerializer(serializers.Serializer):
    site_active_funds = serializers.FloatField(min_value=0)


class UpdateDinamicSiteFundsEndpointSerializer(serializers.Serializer):
    delta_amount = serializers.FloatField(min_value=1)
    for_cases = serializers.BooleanField(default=False)
