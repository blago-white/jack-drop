import pprint

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
            "redirect_url": f"https://jackdrop.online/replenish/?d=1&s=1&a={data.amount_from}&id={tid}",
            "customer_name": data.username,
            "currency": "rub",
            "payeer_identifier": str(data.user_id),
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
            print(response.status_code, response.headers, response.raw)

            raise ValidationError("Error with payment creating")

        result = response.json()

        return response.ok, result

    def create_crypto(self, data: CreateTransactionData,
                      tid: int,
                      payeer_type: str = "ftd"):
        body = {
            "user_uuid": self._credentals.api_user_id,
            "merchant_id": str(tid),
            "amount": int(data.amount_from),
            "callback_url": "https://jackdrop.online/transactions/payments/callback/",
            "redirect_url": f"https://jackdrop.online/replenish/?d=1&s=1&a={data.amount_from}&id={tid}",
            "customer_name": data.username,
            "currency": "crypto",
            "payeer_identifier": str(data.user_id),
            "payeer_ip": data.user_ip,
            "payeer_type": payeer_type,
            "payment_method": "crypto"
        }

        pprint.pprint(body)
        print(self.CREATE_ENDPOINT)

        response = requests.post(
            url=self.CREATE_ENDPOINT,
            headers={
                "Content-Type": "application/json",
                "Signature": self._get_signature(body=body)
            },
            data=body
        )

        print(body, self._get_signature(body=body))

        if not response.ok:
            print(response.status_code, response.text)

            raise ValidationError("Error with payment creating")

        result = response.json()

        return response.ok, result

    def _get_signature(self, body: dict) -> str:
        return hashlib.sha1((self._credentals.apikey + str(body).replace(" ", "")).encode()).hexdigest()
