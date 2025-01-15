import json

import requests
from rest_framework.exceptions import ValidationError
from django.conf import settings

from .transfer.products import DepositCallback


class ProductsApiService:
    routes = settings.PRODUCTS_MICROSERVICE_ROUTES

    def send_deposit_callback(self, callback: DepositCallback) -> dict:
        body = dict(
            amount=callback.deposit_original_amount,
            deposit_id=callback.deposit_id,
            user_id=callback.user_id
        )

        response = requests.post(
            url=self.routes.get("deposit-callback"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(body)
        )

        print("PRODUCTS DEPOSIT CALLBACK: "
              f"{body}"
              f"{response.status_code=}")

        if not response.ok:
            raise ValueError("Error sending depo callback")

        return True

    def get_deposit_free_case(self, deposit_amount: float) -> dict:
        response = requests.get(
            url=self.routes.get("get-free-deposit-case").format(
                deposit=deposit_amount
            ),
        )

        if not response.ok and response.status_code == 400:
            return

        elif not response.ok:
            raise ValidationError("Error receiving free deposit case")

        return response.json()
