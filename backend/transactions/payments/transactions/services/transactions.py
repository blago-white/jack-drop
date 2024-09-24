import requests
import hashlib
import json

from rest_framework.exceptions import ValidationError
from django.conf import settings

from .transfer import ApiCredentals, CreateTransactionData


class TransactionApiService:
    CREATE_ENDPOINT = settings.PAYMENT_SERVICE_URLS["create"]
    CANCEL_ENDPOINT = settings.PAYMENT_SERVICE_URLS["cancel"]

    def __init__(self, credentals: ApiCredentals):
        self._credentals = credentals

    def create(self, tid: int, data: CreateTransactionData):
        body = {
            "pricing": {
                "local": {
                    "amount": data.amount_from,
                    "currency": "RUB"
                }
            },
            "invoiceId": str(tid),
            "callbackUrl": settings.WEBHOOK_URL,
            "redirectUrl": settings.SUCCESS_URL,
            "cancelUrl": settings.FAILED_URL
        }

        headers = {
            "Authorization": settings.PAYMENT_SERVICE_AUTH_HEADER,
            "Content-Type": "application/json"
        }

        response = requests.post(self.CREATE_ENDPOINT,
                                 headers=headers,
                                 data=json.dumps(body))

        response_body = response.json()

        print("=====BODY", response_body, "|", body, type(body))
        print(f"HEADERS: {headers}")
        print(f"BODY: {body}")
        print(response.status_code)

        if not response.ok:
            return False, response_body.get("description")

        return True, response_body

    def cancel(self, foreign_transaction_id: str):
        headers = {
            "Authorization": settings.PAYMENT_SERVICE_AUTH_HEADER,
            "Content-Type": "application/json"
        }

        response = requests.post(self.CANCEL_ENDPOINT.format(
            foreign_transaction_id
        ), headers=headers, data=body)

        if not response.ok:
            raise ValidationError("Something went wrong!", code=500)
