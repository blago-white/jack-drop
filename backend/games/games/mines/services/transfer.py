from dataclasses import dataclass


@dataclass
class FundsDifference:
    user_funds_diff: float
    site_active_funds_per_hour_diff: float


@dataclass
class MinesGameRequest:
    count_mines: int
    user_advantage: float
    user_deposit: float | int
    site_active_funds_per_hour: float


@dataclass
class MinesGameResult:
    is_win: bool
    funds_diffirence: FundsDifference
    loss_step: int = None
