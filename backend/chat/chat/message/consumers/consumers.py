import json

from channels.generic.websocket import AsyncWebsocketConsumer

from message import django_logger

from message.serializers import MessageSerializer
from message.services.messages import BaseMessagesService, MessagesService


__all__ = ["ChatConsumer"]


class ChatConsumer(AsyncWebsocketConsumer):
    _CHAT_GROUP_NAME = "message"
    _MESSAGE_TYPE = "chat_message"
    _service: BaseMessagesService

    def __init__(self, *args,
                 service: BaseMessagesService = MessagesService(),
                 **kwargs):
        self._service = service
        super().__init__(*args, **kwargs)

    async def connect(self):
        django_logger.debug(f"Add new channel {self.channel_name}")

        await self.channel_layer.group_add(self._CHAT_GROUP_NAME, self.channel_name)
        await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        message: MessageSerializer = MessageSerializer(
            data=json.loads(text_data)
        )

        django_logger.debug(f"Receive WS message: {message}")

        if not message.is_valid():
            return await self.channel_layer.group_send(
                group=self._CHAT_GROUP_NAME,
                message=dict(
                    type=self._MESSAGE_TYPE,
                    message=json.dumps(message.errors)
                )
            )

        saved_message = await message.save()

        django_logger.debug(f"Saved message: {saved_message}")

        message = dict(type=self._MESSAGE_TYPE,
                       message=json.dumps(message.data)
                       )

        await self.channel_layer.group_send(group=self._CHAT_GROUP_NAME,
                                            message=message
                                            )

    async def disconnect(self, code):
        django_logger.debug(f"Disconnect channel: {self.channel_name}")

        await self.channel_layer.group_discard(self._CHAT_GROUP_NAME,
                                               self.channel_name)

    async def chat_message(self, message: dict[str, dict]):
        await self.send(message.get("message"))
