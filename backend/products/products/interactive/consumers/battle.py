import json
from logging import getHandlerByName

from channels.generic.websocket import JsonWebsocketConsumer

from games.repositories.api.battle import BattleRequestApiRepository
from games.repositories.api.users import UsersApiRepository

from .utils import get_serialized_message
from .messages import InputMessage, CreateBattleRequest, ConnectToRequest


"""
    battle_repository = BattleRequestApiRepository()
    users_repository = UsersApiRepository()

    serializer_class = BattleRequestApiViewSerializer

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get(user_request=request)

        created = self.battle_repository.create(
            battle_case_id=request.data.get("battle_case_id"),
            user_data=user_data
        )

        return self.get_201_response(
            data=created
        )
"""


django_logger = getHandlerByName("django")


class BattleAsyncConsumer(JsonWebsocketConsumer):
    _MESSAGE_TYPE = "battle_message"

    _users_repository: UsersApiRepository
    _battle_api_repository: BattleRequestApiRepository

    def __init__(
            self, *args,
            users_repository: UsersApiRepository = UsersApiRepository(),
            battle_api_repository: BattleRequestApiRepository = BattleRequestApiRepository(),
            **kwargs):
        self._battle_api_repository = battle_api_repository
        self._users_repository = users_repository
        super().__init__(*args, **kwargs)

    def connect(self):
        # django_logger.debug(f"Add new channel {self.channel_name}")

        self.channel_layer.group_add("_", self.channel_name)
        super().connect()


    def receive(self, text_data=None, bytes_data=None, **kwargs):
        print("RECEIVE", text_data, bytes_data)

        # print(self.scope.get("user").username)

        message: InputMessage = get_serialized_message(
            message=json.loads(text_data)
        )

        if message.message_type == CreateBattleRequest:
            result = self.on_create(message=message,
                                    user_data=self.scope.get("user"))

        elif message.message_type == ConnectToRequest:
            result = self.on_connect_to_request(
                message=message,
            )
        else:
            result = None

        self.channel_layer.group_send(
            group="_",
            message=result
        )

    def on_create(self, message: InputMessage, user_data: dict):
        return self._battle_api_repository.create(
            battle_case_id=message.payload.battle_case_id,
            user_data=user_data,
        )

    def on_connect_to_request(self, message: InputMessage):
        return message

    def disconnect(self, code):
        django_logger.debug(f"Disconnect channel: {self.channel_name}")

        self.channel_layer.group_discard("_", self.channel_name)

    def battle_message(self, message: dict[str, dict]):
        self.send(message.get("message"))
