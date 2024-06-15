from dataclasses import dataclass

from common.services.api.transfer import CaseData, CaseItem


@dataclass
class UserAdvantage:
    advantage: float | int = 0


@dataclass
class BattleGameRequest:
    players_advantage: list[UserAdvantage, UserAdvantage]
    site_active_fund_hour: float | int
