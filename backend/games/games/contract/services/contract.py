from common.services.base import BaseModelService

from ..models import Contract
from .shift import ContractShiftService
from .award import RelevantItemsService


class ContractService(BaseModelService):
    default_model = Contract
    _shift_service: ContractShiftService = ContractShiftService()
    _award_service: RelevantItemsService = RelevantItemsService()

    def __init__(self, *args,
                 contract_shift_service: ContractShiftService,
                 award_service: ContractShiftService,
                 **kwargs):
        self._shift_service = contract_shift_service or self._shift_service
        self._award_service = award_service or self._award_service

        super().__init__(*args, **kwargs)

    def complete_contract(self, granted_amount: int):
        granted_amount -= self._shift_service.get()

        win = self._award_service.get_close_by_price(price=granted_amount)

        self._model.objects.create(
            granted_amount=granted_amount,
            result_item=win.id
        )

        return win
