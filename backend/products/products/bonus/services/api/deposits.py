import json

import requests

from common.services.api.base import BaseApiService

from bonus.serializers import UserDepositValidationSerializer


class UserDepositsApiService(BaseApiService):
    default_endpoint_serializer_class = UserDepositValidationSerializer

    def validate(self, serialized: UserDepositValidationSerializer):
        response = requests.get(
            url=self._routes.get("validate_deposit"),
            data=json.dumps(serialized.data),
            headers={"Content-Type": "application/json"}
        )

        return response.ok
