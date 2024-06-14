from rest_framework.test import APITestCase

from common.services.api.states import FundsState
from .mock import ShiftServiceMock
from ..services.upgrade import UpgradeService


class UpgradeServiceTestCase(APITestCase):
    def test_upgrade(self):
        service = UpgradeService(shift_service=ShiftServiceMock())

        for c in range(10):
            self.assertFalse(service.make_upgrade(
                user_id=1,
                granted_amount=500,
                receive_amount=5000/(c+1),
                funds_state=FundsState(
                    usr_advantage=100,
                    site_active_funds_per_hour=100*c,
                )
            ))
