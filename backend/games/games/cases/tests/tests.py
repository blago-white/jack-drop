from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from .mock import DropCaseItemApiViewMock


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
        case_price = 300
        pricing = {
            1: 500,
            2: 200,
            3: 300
        }

        request = self.factory.post(
            path=reverse("drop-item-view"),
            data={
                "case_id": 1,
                "items": [
                    {"id": 1,
                     "rate": 20,
                     "price": pricing[1]},
                    {"id": 2,
                     "rate": 50,
                     "price": pricing[2]},
                    {"id": 3,
                     "rate": 30,
                     "price": pricing[3]}
                ],
                "funds": {
                    "user_advantage": advantage,
                    "site_active_funds_per_hour": 1340,
                },
                "price": case_price
            }
        )

        response = DropCaseItemApiViewMock.as_view()(request)

        return (case_price - pricing[response.data.drop_item("item_id")]) <= 0
