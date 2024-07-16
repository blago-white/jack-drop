from accounts.repositories.advantage import AdvantageRepository
from common.api.default import DefaultUpdateApiView, DefaultCreateApiView
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
        balance_result = self.balance_repository.update_hidden_balance(
            client_id=self.get_requested_pk(),
            delta_amount=self.request.get("delta_amount")
        )

        if not balance_result.get("ok"):
            return self.get_400_response(data=balance_result)

        self.advantage_repository.update(
            user_id=self.get_requested_pk(),
            delta_amount=self.request.get(
                "delta_amount"
            ))

        return self.get_201_response(data=balance_result)


class AddDepositApiView(BaseDetailedCreateApiViewMixin, DefaultCreateApiView):
    repository = DepositRepository()
    serializer_class = repository.default_serializer_class
    _client_id_param_name = "user_id"
    _deposit_amount_param_name = "amount"

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            data=self.repository.create(
                client_id=self.get_requested_pk(),
                amount=self._get_deposit_amount()
            )
        )

    def get_requested_pk(self) -> int:
        return self.request.data.get(self._client_id_param_name)

    def _get_deposit_amount(self) -> int:
        return self.request.data.get(self._deposit_amount_param_name)
