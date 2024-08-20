from dataclasses import dataclass


@dataclass
class ApiCredentals:
    apikey: str
    api_user_id: str


@dataclass
class CreateTransactionData:
    user_id: int
    user_ip: str
    username: str
    mehtod: str
    amount_from: float
