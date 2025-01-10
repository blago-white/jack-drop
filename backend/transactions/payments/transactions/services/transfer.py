import datetime
from dataclasses import dataclass

from ..models import PaymentStatus, PaymentCurrency


@dataclass
class ApiCredentals:
    merchant_id: str
    secret_key: str


@dataclass
class CreateTransactionData:
    user_login: str
    amount_from: float
    currency: PaymentCurrency[str]


@dataclass
class UpdateTransactionData:
    status: PaymentStatus = None
    payment_method: str = None
    currency: str = None
    expired_at: datetime.datetime = None
