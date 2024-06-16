from rest_framework import serializers

from .site import SiteFundsSerializer
from .users import UserAdvantageIdSerializer


class MinesGameRequestSerializer(serializers.Serializer):
    count_mines = serializers.IntegerField(allow_null=False,
                                           required=True,
                                           min_value=1,
                                           max_value=24)

    user_funds = UserAdvantageIdSerializer(required=True)
    user_deposit = serializers.FloatField(min_value=1)

    site_funds = SiteFundsSerializer(required=True)


class MinesGameRequestViewSerializer(serializers.Serializer):
    count_mines = serializers.IntegerField(allow_null=False,
                                           required=True,
                                           min_value=1,
                                           max_value=25)

    user_deposit = serializers.FloatField(min_value=1)
