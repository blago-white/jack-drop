from dataclasses import dataclass


@dataclass
class ApiCredentals:
    pub: str
    private: str


@dataclass
class CreateTransactionData:
    user_id: int
    from_: str
    to: str
    amount_from: float
    recipient_addres: str
