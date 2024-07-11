from rest_framework.serializers import ModelSerializer

from items.serializers import ItemSerializer
from cases.serializers.case import CaseSerializer

from games.models import GameResult


class GameResultsSerializer(ModelSerializer):
    related_item_first = ItemSerializer(allow_null=True, required=False)
    related_item_second = ItemSerializer(allow_null=True, required=False)
    related_case = CaseSerializer(allow_null=True, required=False)

    class Meta:
        model = GameResult
        fields = "__all__"
