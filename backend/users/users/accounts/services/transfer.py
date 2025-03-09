from dataclasses import dataclass


@dataclass
class LotteryPrize:
    winner_id: int
    prize_item_id: int


@dataclass
class LotteryResult:
    prizes: list[LotteryPrize]
