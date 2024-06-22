from dataclasses import dataclass
from common.services.api.transfer import CaseItem
from common.services.api.states import FundsState


@dataclass
class BattleInfo:
    winner_id: int
    loser_id: int
    battle_case_id: int


@dataclass
class BattleMakeRequest:
    initiator_id: int
    participant_id: int
    battle_case_items: list[CaseItem]
    battle_case_price: int
    battle_case_id: int
    site_active_funds: float


@dataclass
class BattleResult:
    battle_info: BattleInfo
    winner_drop: CaseItem
    loser_drop: CaseItem
    loser_balance_diff: float
    winner_balance_diff: float

    site_funds_diff: float

    def as_json(self) -> dict:
        return {"winner_id": self.battle_info.winner_id,
                "loser_id": self.battle_info.loser_id,
                "battle_case_id": self.battle_info.battle_case_id,
                "dropped_item_winner_id": self.winner_drop.id,
                "dropped_item_loser_id": self.loser_drop.id,
                "loser_balance_diff": self.loser_balance_diff,
                "winner_balance_diff": self.winner_balance_diff}
