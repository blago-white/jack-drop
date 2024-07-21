from dataclasses import dataclass

from common.services.api.states import FundsState, FundsDifference
from common.services.api.transfer import DetailedCaseItem, CaseData, \
    DetailedCaseData


@dataclass
class WheelGameData:
    items: list[DetailedCaseItem | DetailedCaseData]


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
    items: list[DetailedCaseData]

    def __init__(self, items: list[DetailedCaseData]):
        self.items = self._convert_data(items=items)

    @staticmethod
    def _convert_data(items: list[dict]) -> list[DetailedCaseData]:
        return [
            DetailedCaseData(id=case.get("id"),
                             title=case.get("title"),
                             image_path=case.get("image_path"),
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
class CaseDiscountResult:
    case: CaseData
    discount: int

    def as_json(self):
        return {
            "case": self.case.as_json(),
            "discount": self.discount
        }


@dataclass
class FortuneWheelGameResult:
    funds_diff: FundsDifference
    winning_item: DetailedCaseItem | CaseDiscountResult
    user_id: int
    winning_type: str


@dataclass
class CaseDiscountWinningItem:
    case_data: CaseData
    discount: int
