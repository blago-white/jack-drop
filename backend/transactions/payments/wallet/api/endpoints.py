from rest_framework.request import Request

from common.views.api import BaseCreateApiView
from ..repositories.wallet import WalletRepository


class PayWalletApiView(BaseCreateApiView):
    repository = WalletRepository()

    def create(self, request: Request, *args, **kwargs):
        to = request.data.get("to")
        amount = request.data.get("amount_trx")

        return self.get_201_response(
            data=self.repository.pay(
                to=to,
                amount_trx=amount
            )
        )
