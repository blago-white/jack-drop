from dataclasses import dataclass

from common.services.api.states import FundsDifference


@dataclass
class MinesGameRequest:
    count_mines: int
    user_advantage: float
    user_deposit: float | int
    site_active_funds: float


@dataclass
class MinesGameResult:
    is_win: bool
    funds_diffirence: FundsDifference
    loss_step: int = None
