import json

import requests
from django.conf import settings

from .transfer import (ApiCredentals,
                       NicepayCreateTransactionData,
                       SkinifyCreateTransactionData)


class NicepayTransactionApiService:
    CREATE_ENDPOINT = settings.PAYMENT_SERVICE_URLS["nicepay-create"]

    def __init__(self, credentals: ApiCredentals):
        self._credentals = credentals

    def create(
            self, tid: int,
            data: NicepayCreateTransactionData
    ) -> tuple[bool, dict | str]:
        has_free_case = bool(data.free_deposit_case)

        endpoint_url = (settings.SUCCESS_URL
                        if has_free_case else
                        settings.SUCCESS_URL_WITHOUT_FREE_CASE)

        body = {
            "merchant_id": self._credentals.merchant_id,
            "secret": self._credentals.secret_key,
            "order_id": tid,
            "customer": data.user_login,
            "amount": data.amount_from * 100,
            "currency": data.currency,
            "description": f"Пополнение JackDrop на {data.amount_from} {data.currency}",
            "success_url": endpoint_url.format(a=data.amount_from),
            "fail_url": settings.FAILED_URL,
        }

        response = requests.post(self.CREATE_ENDPOINT,
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(body))

        response_body = response.json().get("data")

        if (not response.ok) or (response_body.get("status") == "error"):
            return False, response_body.get("message")

        return True, response_body


class SkinifyTransactionApiService:
    CREATE_ENDPOINT = settings.PAYMENT_SERVICE_URLS["skinify-create"]
    CALLBACK_ENDPOINT = settings.SKINIFY_CALLBACK_URL

    def __init__(self, credentals: ApiCredentals):
        self._credentals = credentals

    def create(
            self, tid: int,
            data: SkinifyCreateTransactionData):
        endpoint_url = settings.SUCCESS_URL_WITHOUT_FREE_CASE

        body = {
            "deposit_id": str(tid),
            "steam_id": data.steam_id,
            "trade_url_token": data.trade_token,
            "priority_game": "rust",
            "result_url": self.CALLBACK_ENDPOINT,
            "success_url": endpoint_url.format(a=data.amount_from),
        }

        response = requests.post(
            self.CREATE_ENDPOINT,
            headers={
                "Content-Type": "application/json",
                "Token": self._credentals.skinify_apikey
            },
            data=json.dumps(body)
        )

        response_body = response.json()

        if (not response.ok) or (response_body.get("status") == "error"):
            return False, response_body.get("error_message")

        return True, response_body
