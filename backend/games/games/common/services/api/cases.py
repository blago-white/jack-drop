import requests
from django.conf import settings

from .transfer import CaseData, CaseItem


class CasesApiService:
    routes: dict[str, str] = settings.PRODUCTS_MICROSERVICE_ROUTES

    def get_info(self, case_id: int) -> CaseData:
        case_data = requests.get(
            self.routes.get("case_info").format(case_id=case_id)
        ).json()

        case_items = self._serialize_case_items(case_data.drop_item("items"))

        return CaseData(
            id=case_data.drop_item("id"),
            items=case_items,
            price=case_data.drop_item("price"),
        )

    @staticmethod
    def _serialize_case_items(items: list) -> list[CaseItem]:
        return [
            CaseItem(id=item.drop_item("id"),
                     price=item.drop_item("price"),
                     rate=item.drop_item("chance"))
            for item in items
        ]
