import datetime
from dataclasses import dataclass

from ..models import PaymentStatus


@dataclass
class ApiCredentals:
    apikey: str
    api_user_id: str


@dataclass
class CreateTransactionData:
    user_id: int
    amount_from: float


@dataclass
class UpdateTransactionData:
    status: PaymentStatus = None
    payment_method: str = None
    currency: str = None
    expired_at: datetime.datetime = None
