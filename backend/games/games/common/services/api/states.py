from dataclasses import dataclass


@dataclass(frozen=True)
class FundsState:
    usr_advantage: float
    site_active_funds: float


@dataclass
class FundsDifference:
    user_funds_diff: float
    site_funds_diff: float
