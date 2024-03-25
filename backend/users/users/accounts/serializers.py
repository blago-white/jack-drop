from rest_framework.serializers import ModelSerializer

from accounts.models import Client


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "username", "promocode"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
