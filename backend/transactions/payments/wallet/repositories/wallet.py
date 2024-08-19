from common.repositories.base import BaseRepository

from ..services.wallet import TronWalletApiService


class WalletRepository(BaseRepository):
    _ONE_TRON = 1000000
    _service = TronWalletApiService()

    def pay(self, to: str, amount_trx: float):
        amount = self._ONE_TRON * amount_trx

        sended = self._service.send(amount=amount, wallet=to)

        return sended
