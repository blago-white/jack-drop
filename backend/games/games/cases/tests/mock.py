from django.http import HttpRequest

from ..api.endpoints import DropCaseItemApiView
from ..repositories.drop import CaseItemDropRepository
from ..services.api.transfer import CaseData
from ..services.api.users import UsersApiService
from ..services.api.cases import CasesApiService
from ..services.api.transfer import CaseData, CaseItem


class CasesWebServiceMock(CasesApiService):
    _case_data = CaseData(
        id=1,
        items=[
            CaseItem(id=1, rate=0.2, price=500),
            CaseItem(id=2, rate=0.5, price=200),
            CaseItem(id=3, rate=0.3, price=300)
        ],
        price=300
    )

    def __init__(self, case_data: CaseData = None):
        self._case_data = case_data or self._case_data

    def get_info(self, case_id: int) -> CaseData:
        return self._case_data


class UsersWebServiceMock(UsersApiService):
    _advantage: float

    def __init__(self, advantage: int = 0):
        self._advantage = advantage

    def get_advantage(self, user_request: HttpRequest) -> float:
        return self._advantage


class DropCaseItemApiViewMock(DropCaseItemApiView):
    repository = CaseItemDropRepository(
        products_web_service=CasesWebServiceMock(),
        users_web_service=UsersWebServiceMock()
    )

    def __init__(self, repository: CaseItemDropRepository = None, **kwargs):
        self.request = repository or self.repository

        super().__init__(**kwargs)
