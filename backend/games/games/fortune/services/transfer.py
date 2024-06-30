from dataclasses import dataclass
from abc import ABCMeta

from common.services.api.states import FundsState, FundsDifference
from common.services.api.transfer import DetailedCaseItem, CaseData


@dataclass
class WheelGameData:
    items: list[DetailedCaseItem | CaseData]


@dataclass
class FortuneWheelCaseItemData:
    items: list[DetailedCaseItem]

    def __init__(self, items: list[DetailedCaseItem]):
        self.items = self._convert_data(items=items)

    @staticmethod
    def _convert_data(items: list[dict]) -> list[DetailedCaseItem]:
        return [
            DetailedCaseItem(id=item.get("id"),
                             price=item.get("price"),
                             rate=None,
                             title=item.get("title"),
                             image_path=item.get("image_path")
                             ) for item in items
        ]


@dataclass
class FortuneWheelCaseData:
    items: list[CaseData]

    def __init__(self, items: list[CaseData]):
        self.items = self._convert_data(items=items)

    @staticmethod
    def _convert_data(items: list[dict]) -> list[CaseData]:
        return [
            CaseData(id=case.get("id"),
                     price=case.get("price"),
                     items=[]) for case in items
        ]


@dataclass
class FortuneWheelTypeGameRequest:
    funds_state: FundsState
    min_item_price: float


@dataclass
class FortuneWheelGameRequest:
    funds_state: FundsState
    winning_type: str
    user_id: int
    data: WheelGameData


@dataclass
class FortuneWheelGameResult:
    funds_diff: FundsDifference
    winning_item: DetailedCaseItem | CaseData
    user_id: int
    winning_type: str


@dataclass
class CaseDiscountWinningItem:
    case_data: CaseData
    discount: int
