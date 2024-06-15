from .messages import InputMessage


def get_serialized_message(message: dict) -> InputMessage:
    return InputMessage(
        message_type=message["type"],
        payload=message["payload"]
    )
