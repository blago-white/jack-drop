from dataclasses import dataclass, field
from time import time

from ..services.api.transfer import CaseItem


@dataclass(frozen=True)
class FoundsState:
    usr_advantage: float
    site_active_hour_funds: float
    daytime: float = field(default_factory=time)


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
