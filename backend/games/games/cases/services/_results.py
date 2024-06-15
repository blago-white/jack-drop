from dataclasses import dataclass


@dataclass(frozen=True)
class FundsDeltaResult:
    site_funds_delta: float
    user_funds_delta: float
