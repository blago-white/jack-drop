from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from common.services.api.transfer import CaseData, CaseItem
from .mock import DropCaseItemApiViewMock, CasesWebServiceMock, \
    UsersWebServiceMock
from ..repositories.drop import CaseItemDropRepository


class DropCaseItemApiViewTestCase(APITestCase):
    factory: APIRequestFactory

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_response(self):
        win_results = [self._test_game(advantage=-1000) for _ in range(10)]

        loss_results = [self._test_game(advantage=1000) for _ in range(10)]

        self.assertTrue(
            (win_results.count(True) >= win_results.count(False)) or
            (loss_results.count(False) >= loss_results.count(True))
        )

    def _test_game(self, advantage: int) -> bool:
        request = self.factory.get(
            path=reverse("drop-item-view", kwargs={"case_id": 1}),
            headers={
                "Authorization": ""
            }
        )

        case_price = 300
        pricing = {
            1: 500,
            2: 200,
            3: 300
        }

        repository = CaseItemDropRepository(
            products_web_service=CasesWebServiceMock(
                case_data=CaseData(
                    id=1,
                    items=[
                        CaseItem(id=1, rate=0.2, price=pricing[1]),
                        CaseItem(id=2, rate=0.5, price=pricing[2]),
                        CaseItem(id=3, rate=0.3, price=pricing[3])
                    ],
                    price=case_price
                )
            ),
            users_web_service=UsersWebServiceMock(advantage=advantage)
        )

        DropCaseItemApiViewMock.repository = repository

        response = DropCaseItemApiViewMock.as_view()(request)

        return (case_price - pricing[response.data.drop_item("item_id")]) <= 0
