import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from cases.repositories.items import CasesItemsRepository
from games.repositories.api.battle import BattleRequestApiRepository, \
    BattleApiRepository
from .messages import InputMessage, CreateBattleRequest, ConnectToRequest, \
    CancelBattleRequest, ListBattleRequests
from .utils import get_serialized_message


class BattleRequestConsumer(JsonWebsocketConsumer):
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
            cases_items_repository: CasesItemsRepository = CasesItemsRepository(),
            **kwargs):
        self._battle_request_api_repository = battle_request_api_repository
        self._battle_api_repository = battle_api_repository
        self._case_items_repository = cases_items_repository

        super().__init__(*args, **kwargs)

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        message: InputMessage = get_serialized_message(
            message=json.loads(text_data)
        )

        response_type = None

        if message.message_type == CreateBattleRequest:
            result = self.on_create(message=message)
            response_type = "create"

        elif message.message_type == CancelBattleRequest:
            result = self.on_cancel()
            response_type = "cancel"

        elif message.message_type == ConnectToRequest:
            self.battle_case_id = message.payload.get("battle_case_id")

            result = self.on_start_battle(
                initiator_id=message.payload.get("initiator_id")
            )
            response_type = "result"
        elif message.message_type == ListBattleRequests:
            self.battle_case_id = message.payload.get("battle_case_id")
            result = self.on_retrieve_battles()
            response_type = "list"

        else:
            result = {"success": False, "error": "Not correct msg type"}

        if self.group_name:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "battle_message",
                    "message": json.dumps({"result": result,
                                           "response_type": response_type})
                }
            )

            if self._count_connections_for_group() == 2:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name, {"type": "disconnect"}
                )

        else:
            self.send_json(content={"result": result,
                                    "response_type": response_type})

    def on_create(self, message: InputMessage) -> dict:
        user_data = self.scope.get("user")

        self.battle_case_id = message.payload.battle_case_id
        self.initiator_id = user_data.get("id")

        self.group_name = self._get_group_name()

        print("CONNECT GROUP NAME", self.group_name, self.initiator_id, self.battle_case_id)

        try:
            result = self._battle_request_api_repository.create(
                battle_case_id=message.payload.battle_case_id,
                user_data=user_data,
            )
        except Exception as e:
            result = {"success": False, "error": e.detail, "fatal": True}

        if result.get("success"):
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
        else:
            self.group_name = None

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

    def on_start_battle(self, initiator_id: int):
        if initiator_id is None:
            return {"success": False, "error": "Battle request not found"}

        self.initiator_id = initiator_id
        self.group_name = self._get_group_name()

        if self._count_connections_for_group() == 0:
            return {"success": False, "error": "Battle request not found"}

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        try:
            return {
                "data": self._battle_api_repository.make(
                    battle_case_id=self.battle_case_id,
                    initiator_id=self.initiator_id,
                    participant_data=self.scope.get("user")
                ),
                "case_items": self._case_items_repository.get_all_by_case(
                    case_pk=self.battle_case_id
                ),
                "success": True
            }
        except Exception as e:
            return {
                "data": {
                    "detail": repr(e)
                },
                "error": "Error with battle, try again",
                "success": False
            }

    def on_retrieve_battles(self) -> list[dict]:
        return self._battle_request_api_repository.get_by_case(
            case_id=self.battle_case_id
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
            print("FAIL GROUP NAME", self.battle_case_id, self.initiator_id)
            return


        return f"{self.battle_case_id}-{self.initiator_id}"
