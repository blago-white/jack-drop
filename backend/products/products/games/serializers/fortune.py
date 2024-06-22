from rest_framework import serializers
from .site import SiteFundsSerializer
from .users import UserAdvantageIdSerializer


class PrizeRequestSerializer(serializers.Serializer):
    site_funds = SiteFundsSerializer(required=True)
    user_funds = UserAdvantageIdSerializer()
    type = serializers.CharField(max_length=1)
    additional_data = serializers.JSONField(allow_null=True)


class PrizeTypeRequestSerializer(serializers.Serializer):
    site_funds = SiteFundsSerializer(required=True)
    user_funds = UserAdvantageIdSerializer()
