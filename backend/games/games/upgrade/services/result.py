from dataclasses import dataclass


@dataclass
class UpgradeResult:
    user_balance_diff: float | int
    site_active_funds_per_hour_diff: float | int
    success: bool
