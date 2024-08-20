import requests

from django.conf import settings

from .transfer import ApiCredentals, CreateTransactionData


class TransactionApiService:
    CREATE_ENDPOINT = settings.BOVA_API_URLS["create"]

    def __init__(self, credentals: ApiCredentals):
        self._credentals = credentals

    def create_card(self, data: CreateTransactionData):
        response = requests.post(
            url=self.CREATE_ENDPOINT,
            headers={
                "Content-Type": "application/json",
                "Signature": self._credentals.private
            },
            data={
                "user_uuid": self._credentals.api_user_id,
                "merchant_id": "string",
                "amount": 1000,
                "callback_url": "https://jackdrop.online/transactions/payments/cb/",
                "redirect_url": "https://jackdrop.online/account/",
                # "email": "test@mail.ru",
                # "customer_name": data,
                "currency": "rub",
                "payeer_identifier": data.user_id,
                "payeer_ip": data.user_ip,
                "payeer_type": "ftd",
                "payment_method": "card"
            }
        )

        result = response.json()

        return response.ok, result
