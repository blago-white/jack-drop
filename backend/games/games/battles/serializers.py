from rest_framework.serializers import ModelSerializer, IntegerField, Serializer

from common.serializers import SiteFundsSerializer
from cases.serializers import DropItemSerializer
from .models import BattleRequest, Battle


class BattleRequestSerializer(ModelSerializer):
    class Meta:
        model = BattleRequest
        fields = "__all__"
        read_only_fields = ["id", "start_find_time"]


class MakeBattleSerializer(Serializer):
    initiator_id = IntegerField(required=True)
    participant_id = IntegerField(required=True)
    site_funds = SiteFundsSerializer(required=True)
    battle_case_id = IntegerField(min_value=0)
    battle_case_price = IntegerField(min_value=0)
    battle_case_items = DropItemSerializer(many=True, required=True)


class BattleSerializer(ModelSerializer):
    class Meta:
        model = Battle
        fields = "__all__"
        read_only_fields = ["id", "finished_at"]
