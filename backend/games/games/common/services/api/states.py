from dataclasses import dataclass


@dataclass
class FundsState:
    usr_advantage: float
    site_active_funds: float
    site_active_funds_for_cases: float = None

    def __post_init__(self):
        if self.site_active_funds_for_cases is None:
            self.site_active_funds_for_cases = self.site_active_funds


@dataclass
class FundsDifference:
    user_funds_diff: float
    site_funds_diff: float
