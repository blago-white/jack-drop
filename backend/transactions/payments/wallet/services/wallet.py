from django.conf import settings

from tronpy.tron import Tron


class TronWalletApiService:
    def __init__(self, wallet_address: str = None,
                 private_key: str = None):
        self._self_wallet_address = wallet_address or settings.WALLET_ADDRESS
        self._private_kry = private_key or settings.PRIVATE_KEY
        self._client = Tron(network="nile")  # TODO: SET MAINNETWORK

    def send(self, amount: float, wallet: str):
        raise NotImplementedError("Now cant send TRX")


class IncomePaymentServiceWalletService:
    async def withdraw(self, address: str):
        raise NotImplementedError("Payment service withdraw not implemented!")
