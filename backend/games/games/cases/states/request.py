from dataclasses import dataclass

from common.services.api.states import FundsState
from common.services.api.transfer import CaseItem


@dataclass(frozen=True)
class DropRequest:
    items: list[CaseItem]
    state: FundsState
    case_price: float


@dataclass(frozen=True)
class ResultState:
    dropped_item: CaseItem
    new_site_funds: float
    new_user_funds: float
