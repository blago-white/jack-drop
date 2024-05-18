from rest_framework import serializers


class DroppedCaseItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(min_value=0)
    case_id = serializers.IntegerField(min_value=0)
