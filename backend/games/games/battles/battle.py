from dataclasses import dataclass


@dataclass
class UserAdvantage:
    advantage: float | int = 0


@dataclass
class BattleGameRequest:
    players_advantage: list[UserAdvantage, UserAdvantage]
    site_active_fund_hour: float | int
