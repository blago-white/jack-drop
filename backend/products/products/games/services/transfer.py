from dataclasses import dataclass


@dataclass
class GameResultData:
    user_id: int
    game: str
    is_win: str
    first_item_id: int = None
    case_id: int = None,
    second_item_id: int = None
