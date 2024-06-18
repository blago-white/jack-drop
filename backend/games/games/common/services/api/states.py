from dataclasses import dataclass, field


@dataclass(frozen=True)
class FundsState:
    usr_advantage: float
    site_active_funds: float
