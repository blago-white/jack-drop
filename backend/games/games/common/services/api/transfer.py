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
class DetailedCaseItem:
    id: int
    rate: float
    image_path: str
    title: str
    price: float
    item_id: int = None

    def as_json(self):
        return {
            "id": self.id,
            "item_id": self.item_id,
            "rate": self.rate,
            "image_path": self.image_path,
            "title": self.title,
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


@dataclass
class DetailedCaseData:
    id: int
    title: str
    image_path: str
    items: list[CaseItem]
    price: int

    def as_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "image_path": self.image_path,
            "items": self.items,
            "price": self.price
        }


@dataclass(frozen=True)
class UserData:
    id: int
    advantage: float
