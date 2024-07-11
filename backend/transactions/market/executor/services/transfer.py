from dataclasses import dataclass


@dataclass
class WithdrawResult:
    success: bool
    inventory_item_id: int
