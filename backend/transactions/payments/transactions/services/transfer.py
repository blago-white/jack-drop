import datetime
import typing

from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from common.services.transfer.products import FreeDepositCase
else:
    FreeDepositCase = object

from ..models import PaymentStatus, PaymentCurrency


@dataclass
class ApiCredentals:
    merchant_id: str
    secret_key: str


@dataclass
class NicepayCreateTransactionData:
    user_id: int
    user_login: str
    amount_from: float
    currency: PaymentCurrency
    free_deposit_case: FreeDepositCase | None = None
    promocode: str = None


@dataclass
class SkinifyCreateTransactionData:
    user_id: int
    steam_id: int
    trade_token: str


@dataclass
class UpdateTransactionData:
    status: PaymentStatus = None
    payment_method: str = None
    currency: str = None
    expired_at: datetime.datetime = None
