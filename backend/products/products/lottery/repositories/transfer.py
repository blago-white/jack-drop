from dataclasses import dataclass


@dataclass
class LotteryPrize:
    winner_id: int
    prize_item_id: int

    def as_json(self) -> dict[str, int]:
        return {
            "winner_id": self.winner_id,
            "prize_item_id": self.prize_item_id
        }


@dataclass
class LotteryResult:
    prizes: list[LotteryPrize, LotteryPrize]

    def as_json(self) -> dict[str, list[dict[str, int]]]:
        return {
            "prizes": [
                i.as_json() for i in self.prizes
            ]
        }
