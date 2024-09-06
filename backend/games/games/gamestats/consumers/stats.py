import json

from asgiref.sync import async_to_sync, sync_to_async

from channels.generic.websocket import JsonWebsocketConsumer

from ..repository.stats import GamesStatsRepository


class GamesStatsConsumer(JsonWebsocketConsumer):
    _repository = GamesStatsRepository()
    _GROUP = "_"

    def __init__(
            self, *args,
            repository: GamesStatsRepository = None,
            **kwargs):
        self._repository = repository or self._repository

        super().__init__(*args, **kwargs)

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self._GROUP,
            self.channel_name
        )

        super().connect()

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        self._refresh_stats()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self._GROUP,
            self.channel_name
        )

        super().disconnect(code=code)

    def stats_message(self, message: dict[str, dict]):
        self.send_json(content=message.get("message"))

    def _refresh_stats(self):
        stats = self._repository.get()

        async_to_sync(self.channel_layer.group_send)(
            self._GROUP,
            {
                "type": "stats_message",
                "message": json.dumps(stats)
            }
        )
