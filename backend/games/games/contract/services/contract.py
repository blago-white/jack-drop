from common.services.base import BaseModelService
from .shift import ContractShiftService
from ..models import Contract


class ContractService(BaseModelService):
    default_model = Contract
    _shift_service: ContractShiftService = ContractShiftService()

    def __init__(self, *args,
                 contract_shift_service: ContractShiftService = None,
                 **kwargs):
        self._shift_service = contract_shift_service or self._shift_service

        super().__init__(*args, **kwargs)

    def get_shiftet_amount(self, granted_amount: float) -> float:
        return granted_amount * (self._shift_service.get_shift()/100)

    def save_contract(self, granted_amount: float, result_item: int) -> None:
        self._model.objects.create(
            granted_amount=granted_amount,
            result_item=result_item
        )
