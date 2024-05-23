from dataclasses import dataclass, field
from time import time


@dataclass(frozen=True)
class FundsState:
    usr_advantage: float
    site_active_hour_funds: float
    daytime: float = field(default_factory=time)
