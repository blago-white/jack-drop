from rest_framework import serializers

from common.serializers import SiteFundsSerializer
from cases.serializers import DropItemSerializer
from .models import BattleRequest, Battle


class BattleRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleRequest
        fields = "__all__"
        read_only_fields = ["id", "start_find_time"]


class MakeBattleSerializer(serializers.Serializer):
    initiator_id = serializers.IntegerField(required=True)
    participant_id = serializers.IntegerField(required=True)
    site_funds = serializers.SiteFundsSerializer(required=True)
    battle_case_id = serializers.IntegerField(min_value=0)
    battle_case_price = serializers.IntegerField(min_value=0)
    battle_case_items = serializers.DropItemSerializer(many=True,
                                                       required=True)


class BattleSerializer(serializers.ModelSerializer):
    site_funds_diff = serializers.FloatField()

    class Meta:
        model = Battle
        fields = "__all__"
        read_only_fields = ["id", "finished_at"]
