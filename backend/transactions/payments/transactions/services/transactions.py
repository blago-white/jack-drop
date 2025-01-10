import json
import typing

import requests
from django.conf import settings

from .transfer import ApiCredentals, CreateTransactionData


class TransactionApiService:
    CREATE_ENDPOINT = settings.PAYMENT_SERVICE_URLS["create"]
    CANCEL_ENDPOINT = settings.PAYMENT_SERVICE_URLS["cancel"]

    def __init__(self, credentals: ApiCredentals):
        self._credentals = credentals

    def create(self, tid: int,
               data: CreateTransactionData
               ) -> typing.Collection[bool, dict | str]:
        body = {
            "merchhant_id": self._credentals.merchant_id,
            "secret": self._credentals.secret_key,
            "order_id": tid,
            "customer": data.user_login,
            "amount": data.amount_from,
            "currency": data.currency,
            "description": f"Пополнение JackDrop на {data.amount_from} {data.currency}",
            "success_url": settings.SUCCESS_URL.format(a=data.amount_from),
            "fail_url": settings.FAILED_URL,
        }

        response = requests.post(self.CREATE_ENDPOINT, data=json.dumps(body))

        response_body = response.json().get("data")

        if (not response.ok) or (response_body.get("status") == "error"):
            return False, response_body.get("message")

        return True, response_body
