import requests

from django.conf import settings

from .transfer import ApiCredentals, CreateTransactionData


class TransactionApiService:
    CREATE_ENDPOINT = settings.CHANGELLY_API_URLS["create"]

    def __init__(self, credentals: ApiCredentals):
        self._credentals = credentals

    def create(self, data: CreateTransactionData):
        response = requests.post(
            url=self.CREATE_ENDPOINT,
            headers={
                "X-Api-Key": self._credentals.pub,
                "X-Api-Signature": self._credentals.private
            },
            data={
                "jsonrpc": "2.0",
                "id": data.user_id,
                "method": "createTransaction",
                "params": {
                    "from": data.from_,
                    "to": data.to,
                    "amountFrom": data.amount_from,
                    "address": data.recipient_addres
                }
            }
        )

        result = response.json()

        return response.ok, result
