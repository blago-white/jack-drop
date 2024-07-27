from common.api.default import DefaultRetrieveApiView, DefaultUpdateApiView

from ..repositories.balance import BalanceRepository
from ..serializers import UpdateClientBalanceSerializer


class DisplayedBalanceRetrieveApiView(DefaultRetrieveApiView):
    repository = BalanceRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request, *args, **kwargs):
        client_id = request.user.pk

        data = self.repository.get_displayed_balance(
            client_id=client_id
        )

        return self.get_200_response(
            data=data
        )


class DisplayedBalanceUpdateJWTApiView(DefaultUpdateApiView):
    repository = BalanceRepository()
    serializer_class = UpdateClientBalanceSerializer

    def partial_update(self, request, *args, **kwargs):
        return self.update(*args, request=request, **kwargs)

    def update(self, request, *args, **kwargs):
        client_id = request.user.pk

        data = self.repository.update_displayed_balance(
            client_id=client_id,
            delta_amount=self.request.data.get("delta_amount")
        )

        return self.get_200_response(
            data=data
        )


class DisplayedBalanceUpdateApiView(DefaultUpdateApiView):
    repository = BalanceRepository()
    serializer_class = UpdateClientBalanceSerializer
    pk_url_kwarg = "client_id"

    def update(self, request, *args, **kwargs):
        return self.partial_update(*args, request=request, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        print(self.request.data, "UPDATE BALANCE")

        data = self.repository.update_displayed_balance(
            client_id=self.get_requested_pk(),
            delta_amount=self.request.data.get("delta_amount")
        )

        return self.get_201_response(data=data)
