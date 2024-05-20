from rest_framework import serializers


class GameRequestSerializer(serializers.Serializer):
    granted_item = serializers.IntegerField(allow_null=True)
    granted_balance = serializers.IntegerField(allow_null=True, default=0)

    receive_item = serializers.IntegerField(allow_null=True)
    receive_balance = serializers.IntegerField(allow_null=True, default=0)

    # def clean_receive_item(self):
    #     return
