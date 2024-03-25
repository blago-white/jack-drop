from abc import ABCMeta, abstractmethod

from message.models import Message


class BaseMessagesService(metaclass=ABCMeta):
    _model: Message

    def __init__(self, model: Message = Message):
        self._model = model

    @abstractmethod
    async def get(self, pk: int):
        pass

    @abstractmethod
    async def save(self, username: str, text: str):
        pass

    @abstractmethod
    async def get_all(self):
        pass


class MessagesService(BaseMessagesService):
    async def get(self, pk: int) -> Message:
        return self._model.objects.get(pk=pk)

    async def save(self, username: str, text: str) -> Message:
        return await self._model.objects.acreate(
            username=username,
            text=text
        )

    def get_all(self):
        return self._model.objects.all()
