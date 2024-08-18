from django.conf import settings

from tronpy.tron import Tron


class TronWalletApiService:
    def __init__(self, wallet_addres: str = None,
                 private_key: str = None):
        self._self_wallet_addres = wallet_addres or settings.WALLET_ADDRES
        self._private_kry = private_key or settings.PRIVATE_KEY
        self._client = Tron(network="nile")  # TODO: SET MAINNETWORK

    def send(self, amount: float, wallet: str):
        try:
            private = PrivateKey(bytes.fromhex(self._private_kry))

            transaction = (
                self._client.trx.transfer(self._self_wallet_addres, amount, wallet)
                .memo("Transaction Description")
                .build()
                .inspect()
                .sign(private)
                .broadcast()
            )

            return transaction.txid
        except Exception as exc:
            return exc
