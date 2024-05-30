from rest_framework import serializers

from cases.services.cases import CaseService


class BattleRequestServiceEndpointSerializer(serializers.Serializer):
    initiator_id = serializers.IntegerField(min_value=0)
    battle_case_id = serializers.PrimaryKeyRelatedField(
        queryset=CaseService().get_all()
    )


class BattleRequestApiViewSerializer(serializers.Serializer):
    initiator_id = serializers.IntegerField(min_value=0)
