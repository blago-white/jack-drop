from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository

from ..services.messages import MessagesService
from ..services.transfer import MessageData
from ..serializers import MessageSerializer


class MessagesRepository(BaseRepository):
    default_service = MessagesService()
    default_serializer_class = MessageSerializer

    _service: MessagesService

    def get_all(self, user_id: int, username: str) -> list[dict]:
        data = self._service.get_all_by_user(user_id=user_id,
                                             username=username)

        return self._serializer_class(instance=data, many=True).data

    def add(self, user_id: int, text: str, username: str) -> dict:
        if not (user_id and text):
            raise ValidationError("Require Text of message!")

        added = self._service.add(message=MessageData(
            user_id=user_id,
            text=text,
            username=username
        ))

        return {"ok": True if added else False}
