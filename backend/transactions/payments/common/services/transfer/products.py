from dataclasses import dataclass


@dataclass
class DepositCallback:
    deposit_original_amount: float
    deposit_id: int
    user_id: float
