from dataclasses import dataclass


@dataclass
class UpgradeResult:
    user_balance_diff: float | int
    site_active_funds_diff: float | int
    success: bool
