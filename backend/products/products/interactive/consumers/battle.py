import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from games.repositories.api.battle import BattleRequestApiRepository, \
    BattleApiRepository
from .messages import InputMessage, CreateBattleRequest, ConnectToRequest, \
    CancelBattleRequest
from .utils import get_serialized_message


class BattleRequestAsyncConsumer(JsonWebsocketConsumer):
    _MESSAGE_TYPE = "battle_message"

    _battle_request_api_repository: BattleRequestApiRepository
    _battle_api_repository: BattleApiRepository

    battle_case_id: int = "-1"
    initiator_id: int = None

    group_name: str = None

    def __init__(
            self, *args,
            battle_api_repository: BattleApiRepository = BattleApiRepository(),
            battle_request_api_repository: BattleRequestApiRepository = BattleRequestApiRepository(),
            **kwargs):
        self._battle_request_api_repository = battle_request_api_repository
        self._battle_api_repository = battle_api_repository

        super().__init__(*args, **kwargs)

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        message: InputMessage = get_serialized_message(
            message=json.loads(text_data)
        )

        if message.message_type == CreateBattleRequest:
            result = self.on_create(message=message)

        elif message.message_type == CancelBattleRequest:
            result = self.on_cancel()

        elif message.message_type == ConnectToRequest:
            self.battle_case_id = message.payload.get("battle_case_id")

            result = self.on_start_battle()
        else:
            result = {"success": False, "error": "Not correct msg type"}

        if self.group_name:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "battle_message",
                    "message": json.dumps({"result": result})
                }
            )

            if self._count_connections_for_group() == 2:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name, {"type": "disconnect"}
                )

        else:
            self.send_json(content={"result": result})

    def on_create(self, message: InputMessage) -> dict:
        user_data = self.scope.get("user")

        self.battle_case_id = message.payload.battle_case_id
        self.initiator_id = user_data.get("id")

        self.group_name = self._get_group_name()

        if count_conns := self._count_connections_for_group():
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )
            self.group_name = None

            return {"success": False,
                    "error": f"Battle request now exists ({count_conns})"}

        result = self._battle_request_api_repository.create(
            battle_case_id=message.payload.battle_case_id,
            user_data=user_data,
        )

        if result.get("ok"):
            print("ADDED:", self.group_name)

            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )

            print("CHANNELS:", self.channel_layer.groups)
        else:
            self.group_name = None

        print(result, "RESULT CREATE")

        return result

    def on_cancel(self) -> dict:
        if self._count_connections_for_group() >= 2:
            return {"success": False, "error": "Battle is run now"}
        elif not self.group_name:
            return {"success": True, "not_modified": True}

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

        self.group_name = None

        return self._battle_request_api_repository.cancel(
            initiator_id=self.initiator_id
        )

    def on_start_battle(self):
        initiator_id = [
            i.split("-")[-1]
            for i in self.channel_layer.groups.keys()
            if i.split("-")[0] == str(self.battle_case_id)
        ]

        if not initiator_id:
            return {"success": "False", "error": "Battle request not found"}
        else:
            self.initiator_id = int(initiator_id[0])

        self.group_name = self._get_group_name()

        if self._count_connections_for_group() != 1:
            return {"success": False, "error": "Battle request not found"}

        participant_id = self.scope.get("user").get("id")

        print("ADDED:", self.group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        print("CHANNELS:", self.channel_layer.groups)

        return self._battle_api_repository.make(
            battle_case_id=self.battle_case_id,
            initiator_id=self.initiator_id,
            participant_id=participant_id
        )

    def disconnect(self, code):
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

        super().disconnect(code=code)

    def battle_message(self, message: dict[str, dict]):
        self.send_json(content=message.get("message"))

    def _count_connections_for_group(self):
        count = list(self.channel_layer.groups.keys())

        return len(
            self.channel_layer.groups.get(self.group_name) or []
        )

    def _get_group_name(self) -> str:
        if not (self.battle_case_id and self.initiator_id):
            raise ValueError

        return f"{self.battle_case_id}-{self.initiator_id}"
