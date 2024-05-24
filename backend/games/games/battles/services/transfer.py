from dataclasses import dataclass


@dataclass
class BattleInfo:
    winner_id: int
    loser_id: int
    battle_case_id: int
