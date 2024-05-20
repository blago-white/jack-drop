from time import time
from dataclasses import dataclass, field


@dataclass(frozen=True)
class FoundsState:
    usr_advantage: float
    site_active_hour_funds: float
    daytime: float = field(default_factory=time)
