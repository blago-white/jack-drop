import requests

from common.services.api.base import BaseApiService
from inventory.serializers import ScheduledItemSerializer


class WithdrawScheduleApiService(BaseApiService):
    default_endpoint_serializer_class = ScheduledItemSerializer

    def add(self, serialized: ScheduledItemSerializer) -> dict:
        response = requests.post(
            url=self._routes.get("add_schedule_item"),
            data=serialized.data
        )

        if response.ok:
            result = response.json()

            return result
        return False
