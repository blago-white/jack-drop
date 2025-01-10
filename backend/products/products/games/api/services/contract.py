import requests
from requests.models import Response

from games.serializers.contract import CommitContractSerializer, \
    ShiftedContractAmountSerializer
from common.services.api.base import BaseApiService


class ContractApiService(BaseApiService):
    default_endpoint_serializer_class = CommitContractSerializer

    def get_shifted_amount(self, amount: float) -> float:
        response = requests.get(
            self._routes.get("contract_get_amount"),
            data=ShiftedContractAmountSerializer(instance={
                "granted_amount": amount
            }).data
        )

        return response.json().get("shifted_funds")

    def save_contract(self, serialized: CommitContractSerializer) -> bool:
        response: Response = requests.post(
            self._routes.get("contract_save"),
            data=serialized.data
        )

        return response.status_code == 201
