from dataclasses import dataclass


@dataclass
class MessageData:
    user_id: int
    text: str
    username: str
