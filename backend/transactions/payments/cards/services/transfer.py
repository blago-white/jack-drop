from dataclasses import dataclass


@dataclass
class ApiCredentals:
    apikey: str
    api_user_id: str


@dataclass
class CreateTransactionData:
    user_id: int
    user_ip: str
    from_: str
    to: str
    amount_from: float
    recipient_address: str
