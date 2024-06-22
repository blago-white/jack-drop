from common.api.default import DefaultRetrieveApiView, DefaultUpdateApiView

from ..repositories.balance import BalanceRepository
from accounts.repositories.advantage import AdvantageRepository
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
