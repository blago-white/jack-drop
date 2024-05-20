from dataclasses import dataclass

from common.states import FoundsState

from common.services.api.transfer import CaseItem


@dataclass(frozen=True)
class DropRequest:
    items: list[CaseItem]
    state: FoundsState
    case_price: float


@dataclass(frozen=True)
class ResultState:
    dropped_item: CaseItem
    site_funds_delta: float
    user_funds_delta: float
