from dataclasses import dataclass


@dataclass
class LotteryWinners:
    main_lottery_winner_id: int = -1
    secondary_lottery_winner_id: int = -1
