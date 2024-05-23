from rest_framework import serializers

from common.serializers import UserFundsStateSerializer, SiteFundsSerializer


class MinesGameRequestSerializer(serializers.Serializer):
    count_mines = serializers.IntegerField(allow_null=False,
                                           required=True,
                                           min_value=15)  # TODO: Make constant

    user_funds = UserFundsStateSerializer(required=True)

    site_funds = SiteFundsSerializer(required=True)
