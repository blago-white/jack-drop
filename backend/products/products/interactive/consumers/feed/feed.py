import json
import random

import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from items.services.items import ItemService


class FeedWebsocketConsumer(JsonWebsocketConsumer):
    _DROPS_FEED_GROUP = "_"

    _items_service = ItemService()

    def __int__(self, *args,
                items_service: ItemService = None,
                **kwargs):
        self._items_service = items_service or self._items_service

        super().__int__(*args, **kwargs)

    def connect(self):
        print("___##")

        async_to_sync(self.channel_layer.group_add)(
            self._DROPS_FEED_GROUP,
            self.channel_name
        )

        super().connect()

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        self._send_drop()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self._DROPS_FEED_GROUP,
            self.channel_name
        )

        super().disconnect(code=code)

    def feed_drop_message(self, message: dict[str, dict]):
        self.send_json(content=message.get("message"))

    def _send_drop(self):
        item = self._items_service.get_random()

        async_to_sync(self.channel_layer.group_send)(
            self._DROPS_FEED_GROUP,
            {
                "type": "feed_drop_message",
                "message": json.dumps({
                    "title": item.title,
                    "image": item.image_path,
                    "price": item.price
                })
            }
        )
