from rest_framework.serializers import ModelSerializer

from .models import BattleRequest, Battle


class BattleRequestSerializer(ModelSerializer):
    class Meta:
        model = BattleRequest
        fields = "__all__"
        read_only_fields = ["id", "start_find_time"]


class BattleSerializer(ModelSerializer):
    class Meta:
        model = Battle
        fields = "__all__"
        read_only_fields = ["id", "finished_at"]
