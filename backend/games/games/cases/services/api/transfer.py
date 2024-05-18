from dataclasses import dataclass


@dataclass(frozen=True)
class CaseItem:
    id: int
    rate: float
    price: float


@dataclass
class CaseData:
    id: int
    items: list
    price: int
