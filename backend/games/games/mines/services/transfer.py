from dataclasses import dataclass

from common.services.api.states import FundsDifference


@dataclass
class MinesGameNextStepRequest:
    count_mines: int
    user_advantage: float
    user_deposit: float | int
    user_current_ammount: float
    site_active_funds: float
    step: int


@dataclass
class MinesGameStepResult:
    is_win: bool
    funds_diffirence: FundsDifference
    next_win_factor: int


@dataclass
class MinesGameInitParams:
    user_id: int
    advantage: float
    count_mines: int
    deposit: int
