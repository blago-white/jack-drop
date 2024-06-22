from dataclasses import dataclass


@dataclass(frozen=True)
class CaseItem:
    id: int
    rate: float
    price: float

    def as_json(self):
        return {
            "id": self.id,
            "rate": self.rate,
            "price": self.price
        }


@dataclass(frozen=True)
class CaseData:
    id: int
    items: list[CaseItem]
    price: int

    def as_json(self):
        return {
            "id": self.id,
            "items": self.items,
            "price": self.price
        }


@dataclass(frozen=True)
class UserData:
    id: int
    advantage: float
