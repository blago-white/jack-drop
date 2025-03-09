from dataclasses import dataclass


@dataclass
class LotteryWinners:
    main_lottery_winner_id: int
    secondary_lottery_winner_id: int
