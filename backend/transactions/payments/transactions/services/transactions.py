import requests
import hashlib

from rest_framework.exceptions import ValidationError
from django.conf import settings

from .transfer import ApiCredentals, CreateTransactionData


class TransactionApiService:
    CREATE_ENDPOINT = settings.BOVA_API_URLS["create"]

    def __init__(self, credentals: ApiCredentals):
        self._credentals = credentals

    def create_card(self, data: CreateTransactionData,
                    tid: int,
                    payeer_type: str = "ftd"):
        body = {
            "user_uuid": self._credentals.api_user_id,
            "merchant_id": tid,
            "amount": data.amount_from,
            "callback_url": "https://jackdrop.online/transactions/payments/callback/",
            "redirect_url": f"https://jackdrop.online/pay-success/?a={data.amount_from}",
            "customer_name": data.username,
            "currency": "rub",
            "payeer_identifier": data.user_id,
            "payeer_ip": data.user_ip,
            "payeer_type": payeer_type,
            "payment_method": "card"
        }

        response = requests.post(
            url=self.CREATE_ENDPOINT,
            headers={
                "Content-Type": "application/json",
                "Signature": self._get_signature(body=body)
            },
            data=body
        )

        if not response.ok:
            raise ValidationError("Error with payment creating")

        result = response.json()

        return response.ok, result

    def create_crypto(self, data: CreateTransactionData,
                      tid: int,
                      payeer_type: str = "ftd"):
        body = {
            "user_uuid": self._credentals.api_user_id,
            "merchant_id": tid,
            "amount": data.amount_from,
            "callback_url": "https://jackdrop.online/transactions/payments/callback/",
            "redirect_url": f"https://jackdrop.online/pay-success/?a={data.amount_from}",
            "customer_name": data.username,
            "currency": "crypto",
            "payeer_identifier": data.user_id,
            "payeer_ip": data.user_ip,
            "payeer_type": payeer_type,
            "payment_method": "crypto"
        }

        response = requests.post(
            url=self.CREATE_ENDPOINT,
            headers={
                "Content-Type": "application/json",
                "Signature": self._get_signature(body=body)
            },
            data=body
        )

        if not response.ok:
            raise ValidationError("Error with payment creating")

        result = response.json()

        return response.ok, result

    def _get_signature(self, body: dict) -> str:
        return hashlib.sha1(self._credentals.apikey + str(body).replace(" ", ""))
