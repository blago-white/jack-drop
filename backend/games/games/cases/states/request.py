from dataclasses import dataclass

from common.services.api.states import FundsState
from common.services.api.transfer import DetailedCaseItem


@dataclass(frozen=True)
class DropRequest:
    items: list[DetailedCaseItem]
    state: FundsState
    case_price: float
    early_drops_rate: tuple[int, float]


@dataclass(frozen=True)
class ResultState:
    dropped_item: DetailedCaseItem
    site_funds_delta: float
    user_funds_delta: float
