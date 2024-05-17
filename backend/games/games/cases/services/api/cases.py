import requests

from django.conf import settings

from cases.states.request import DropRequest, FoundsState
from .transfer import CaseData


class CasesApiService:
    routes: dict[str, str] = settings.PRODUCTS_MICROSERVICE_ROUTES

    def get_info(self, case_id: int) -> CaseData:
        case_data = requests.get(
            self.routes.get("case_info").format(case_id=case_id)
        ).json()

        return CaseData(
            id=case_data.get("id"),
            items=case_data.get("items"),
            price=case_data.get("price"),
        )
