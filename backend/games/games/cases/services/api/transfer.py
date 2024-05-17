from dataclasses import dataclass


@dataclass
class CaseData:
    id: int
    items: list
    price: int
