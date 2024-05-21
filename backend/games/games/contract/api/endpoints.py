from common.views.api import DefaultRetrieveApiView, DefaultCreateApiView

from ..repositories.contract import ContractAmountShiftRepository, ContractRepository


class ShiftedContractAmountApiView(DefaultRetrieveApiView):
    repository = ContractAmountShiftRepository
    serializer_class = ContractAmountShiftRepository.default_serializer_class

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get_shifted_amount(request=request)
        )


class SaveContractApiView(DefaultCreateApiView):
    repository = ContractRepository
    serializer_class = ContractRepository.default_serializer_class

    def create(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.save_contract(request=request)
        )
