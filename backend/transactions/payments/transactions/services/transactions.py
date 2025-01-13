import json

import requests
from django.conf import settings

from .transfer import ApiCredentals, CreateTransactionData


class TransactionApiService:
    CREATE_ENDPOINT = settings.PAYMENT_SERVICE_URLS["create"]

    def __init__(self, credentals: ApiCredentals):
        self._credentals = credentals

    def create(self, tid: int,
               data: CreateTransactionData
               ) -> tuple[bool, dict | str]:
        has_free_case = data.free_deposit_case is not None

        body = {
            "merchant_id": self._credentals.merchant_id,
            "secret": self._credentals.secret_key,
            "order_id": tid,
            "customer": data.user_login,
            "amount": data.amount_from * 100,
            "currency": data.currency,
            "description": f"Пополнение JackDrop на {data.amount_from} {data.currency}",
            "success_url": settings.SUCCESS_URL.format(
                **dict(
                    a=data.amount_from,
                    has_free_case=int(has_free_case),
                ) | (dict(
                    free_case_img=data.case_img,
                    free_case_title=data.case_title
                ) if has_free_case else dict())
            ),
            "fail_url": settings.FAILED_URL,
        }

        response = requests.post(self.CREATE_ENDPOINT,
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(body))

        response_body = response.json().get("data")

        if (not response.ok) or (response_body.get("status") == "error"):
            return False, response_body.get("message")

        return True, response_body
