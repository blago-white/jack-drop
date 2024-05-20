import requests

from django.conf import settings

from cases.states.request import DropRequest
from .transfer import CaseData, CaseItem


class CasesApiService:
    routes: dict[str, str] = settings.PRODUCTS_MICROSERVICE_ROUTES

    def get_info(self, case_id: int) -> CaseData:
        case_data = requests.get(
            self.routes.get("case_info").format(case_id=case_id)
        ).json()

        case_items = self._serialize_case_items(case_data.get("items"))

        return CaseData(
            id=case_data.get("id"),
            items=case_items,
            price=case_data.get("price"),
        )

    @staticmethod
    def _serialize_case_items(items: list) -> list[CaseItem]:
        return [
            CaseItem(id=item.get("id"),
                     price=item.get("price"),
                     rate=item.get("chance"))
            for item in items
        ]
