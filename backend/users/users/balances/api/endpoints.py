from common.api.default import DefaultRetrieveApiView

from ..repositories.balance import BalanceRepository


class DisplayedBalanceRetrieveApiView(DefaultRetrieveApiView):
    repository = BalanceRepository()
    serializer_class = repository.default_serializer_class
    pk_url_kwarg = "client_id"

    def retrieve(self, request, *args, **kwargs):
        data = self.repository.get_displayed_balance(
            client_id=self.get_requested_pk()
        )

        return self.get_200_response(
            data=data
        )
