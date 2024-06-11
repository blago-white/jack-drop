from rest_framework.serializers import ModelSerializer, IntegerField

from common.serializers import SiteFundsSerializer, UserFundsStateSerializer
from .models import BattleRequest, Battle


class BattleRequestSerializer(ModelSerializer):
    class Meta:
        model = BattleRequest
        fields = "__all__"
        read_only_fields = ["id", "start_find_time"]


class MakeBattleSerializer(ModelSerializer):
    initiator_data = UserFundsStateSerializer(required=True)
    participant_data = UserFundsStateSerializer(required=True)
    site_funds = SiteFundsSerializer(required=True)
    battle_case_id = IntegerField(min_value=0)


class BattleSerializer(ModelSerializer):
    class Meta:
        model = Battle
        fields = "__all__"
        read_only_fields = ["id", "finished_at"]
