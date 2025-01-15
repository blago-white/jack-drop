import rest_framework.exceptions

from accounts.repositories.advantage import AdvantageRepository
from common.api.default import DefaultUpdateApiView, DefaultCreateApiView, DefaultRetrieveApiView
from common.mixins import BaseDetailedCreateApiViewMixin
from ..repositories.balance import BalanceRepository
from ..repositories.deposits import DepositRepository
from ..serializers import UpdateClientBalanceSerializer


class DisplayedBalanceUpdateApiView(DefaultUpdateApiView):
    balance_repository = BalanceRepository()
    advantage_repository = AdvantageRepository()

    serializer_class = UpdateClientBalanceSerializer
    pk_url_kwarg = "client_id"

    def partial_update(self, request, *args, **kwargs):
        balance_result = self.balance_repository.update_displayed_balance(
            client_id=self.get_requested_pk(),
            delta_amount=self.request.data.get("delta_amount")
        )

        if not balance_result.get("ok"):
            return self.get_400_response(data=balance_result)

        return self.get_201_response(data=balance_result)


class AddDepositApiView(BaseDetailedCreateApiViewMixin, DefaultCreateApiView):
    repository = DepositRepository()
    balance_repository = BalanceRepository()
    serializer_class = repository.default_serializer_class
    pk_url_kwarg = "user_id"
    _deposit_amount_param_name = "amount"

    def create(self, request, *args, **kwargs):
        print(f"RECEIVED DEPO CALLBACK: "
              f"client_id={self.get_requested_pk()}"
              f"amount={self._get_deposit_amount()}"
              f"promocode={request.data.get('promocode')}")

        if request.data.get('promocode'):
            promocode = request.data.get('promocode').upper()
        else:
            promocode = None

        amount, created_deposit = self.repository.create(
            client_id=self.get_requested_pk(),
            amount=self._get_deposit_amount(),
            promocode=promocode
        )

        update_balance = self.balance_repository.update_displayed_balance(
            client_id=self.get_requested_pk(),
            delta_amount=amount
        )

        if not update_balance.get("ok"):
            raise rest_framework.exceptions.ValidationError("Error replenish",
                                                            code=500)

        return self.get_201_response(
            data=created_deposit
        )

    def get_requested_pk(self) -> int:
        return self.request.data.get(self.pk_url_kwarg)

    def _get_deposit_amount(self) -> int:
        return float(self.request.data.get(self._deposit_amount_param_name))


class ValidateUserDepositApiView(DefaultRetrieveApiView):
    repository = DepositRepository()

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.validate(
                deposit_id=request.data.get("deposit_id"),
                deposit_amount=request.data.get("deposit_amount")
            )
        )
