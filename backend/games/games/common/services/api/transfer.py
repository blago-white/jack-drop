from dataclasses import dataclass


@dataclass(frozen=True)
class CaseItem:
    id: int
    rate: float
    price: float


@dataclass(frozen=True)
class CaseData:
    id: int
    items: list
    price: int


@dataclass(frozen=True)
class UserData:
    id: int
    advantage: float
