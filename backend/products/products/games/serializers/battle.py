from rest_framework import serializers

from cases.services.cases import CaseService
from .drop import DropItemSerializer
from .site import SiteFundsSerializer


class BattleRequestServiceEndpointSerializer(serializers.Serializer):
    initiator_id = serializers.IntegerField(min_value=0)
    battle_case_id = serializers.PrimaryKeyRelatedField(
        queryset=CaseService().get_all()
    )


class BattleRequestApiViewSerializer(serializers.Serializer):
    initiator_id = serializers.IntegerField(min_value=0)


class MakeBattleServiceEndpointSerializer(serializers.Serializer):
    initiator_id = serializers.IntegerField(required=True)
    participant_id = serializers.IntegerField(required=True)
    site_funds = SiteFundsSerializer(required=True)
    battle_case_id = serializers.IntegerField(min_value=0)
    battle_case_price = serializers.IntegerField(min_value=0)
    battle_case_items = DropItemSerializer(many=True, required=True)
