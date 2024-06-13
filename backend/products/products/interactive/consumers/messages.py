from dataclasses import dataclass


class _MessageType:
    pass


class CreateBattleRequest(_MessageType):
    pass


class ConnectToRequest(_MessageType):
    pass


class CancelBattleRequest(_MessageType):
    pass


@dataclass
class CreateRequestMessagePayload:
    battle_case_id: int


MESSAGE_TYPE_CODES = {
    "cbr": CreateBattleRequest,
    "ctr": ConnectToRequest,
    "crb": CancelBattleRequest
}


@dataclass
class InputMessage:
    message_type: _MessageType
    payload: dict | CreateRequestMessagePayload

    def __init__(self, message_type: _MessageType, payload: dict):
        if not issubclass(_MessageType, type(message_type)):
            message_type = MESSAGE_TYPE_CODES[message_type]

        self.message_type = message_type

        self.payload = CreateRequestMessagePayload(
            battle_case_id=payload["battle_case_id"],
        ) if message_type == CreateBattleRequest else payload
