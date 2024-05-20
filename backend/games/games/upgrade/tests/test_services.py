from django.test import TestCase
from rest_framework.test import APITestCase

from common.states import FoundsState

from ..services.upgrade import UpgradeService
from .mock import ShiftServiceMock


class UpgradeServiceTestCase(APITestCase):
    def test_upgrade(self):
        service = UpgradeService(shift_service=ShiftServiceMock())

        for c in range(10):
            self.assertFalse(service.make_upgrade(
                user_id=1,
                granted_amount=500,
                receive_amount=5000/(c+1),
                founds_state=FoundsState(
                    usr_advantage=100,
                    site_active_hour_funds=100*c,
                )
            ))
