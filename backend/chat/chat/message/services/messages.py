from abc import ABCMeta, abstractmethod

from common.services.base import BaseModelService
from ..models import Chat, ChatMessage
from .transfer import MessageData


class MessagesService(BaseModelService):
    default_model = Chat
    default_chat_message = ChatMessage

    def __init__(self, *args, chat_message: ChatMessage = None, **kwargs):
        self._chat_message = chat_message or self.default_chat_message

        super().__init__(*args, **kwargs)

    def add(self, message: MessageData) -> ChatMessage:
        chat, created = self._model.objects.get_or_create(
            user_id=message.user_id,
            defaults={"username": message.username}
        )

        message = self._chat_message.objects.create(
            text=message.text,
            username=message.username,
            from_admin=False
        )

        chat.messages.add(message)

        return message

    def get_all_by_user(self, user_id: int, username: str):
        chat, created = self._model.objects.get_or_create(
            user_id=user_id,
            defaults={
                "username": username
            }
        )

        return chat.messages.all()
