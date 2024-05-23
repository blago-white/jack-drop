from rest_framework.request import Request

from common.repositories import BaseRepository
from ..serializers import ShiftedContractAmountSerializer, ContractSerializer
from ..services.contract import ContractService


class ContractAmountShiftRepository(BaseRepository):
    default_service = ContractService()
    default_serializer_class = ShiftedContractAmountSerializer

    _service: ContractService

    def get_shifted_amount(self, request: Request) -> dict:
        serialized: ShiftedContractAmountSerializer = (
            self._serializer_class(data=request.data)
        )

        serialized.is_valid(raise_exception=True)

        shifted = self._service.get_shiftet_amount(
            granted_amount=serialized.data.get("granted_amount")
        )

        return {"shifted_funds": shifted}


class ContractRepository(BaseRepository):
    default_service = ContractService()
    default_serializer_class = ContractSerializer

    _service: ContractService

    def save_contract(self, request: Request) -> dict:
        serialized: ContractSerializer = self._serializer_class(data=request.DATA)

        serialized.is_valid(raise_exception=True)

        return self._serializer_class(instance=self._service.save_contract(
            granted_amount=serialized.data.get_user_info("granted_amount"),
            result_item=serialized.data.get_user_info("result_item")
        )).data
