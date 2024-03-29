from rest_framework import serializers

from .models import Message
from .config import SENDER_USERNAME_MAX_LEN, MESSAGE_MAX_LEN
from .services.messages import BaseMessagesService, MessagesService


class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=SENDER_USERNAME_MAX_LEN,
    )

    text = serializers.CharField(
        max_length=MESSAGE_MAX_LEN
    )

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["id", "date"]

    def __init__(self, *args,
                 service: BaseMessagesService = MessagesService(),
                 **kwargs):
        self._service = service

        super().__init__(*args, **kwargs)

    async def save(self, **kwargs):
        return await self._service.save(
            username=self.validated_data.get("username"),
            text=self.validated_data.get("text")
        )

    async def update(self, **kwargs):
        raise NotImplementedError()
