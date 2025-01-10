import json

import requests
from django.conf import settings

from .transfer.products import DepositCallback


class ProductsApiService:
    routes = settings.PRODUCTS_MICROSERVICE_ROUTES
    _retries_to_abort = 3

    def send_deposit_callback(self, callback: DepositCallback) -> dict:
        if not self._retries_to_abort:
            return False

        response = requests.post(
            url=self.routes.get("deposit-callback"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(dict(
                amount=callback.deposit_original_amount,
                deposit_id=callback.deposit_id,
                user_id=callback.user_id
            ))
        )

        print(response.status_code, response.text)

        if not response.ok:
            self._retries_to_abort -= 1
            return self.send_deposit_callback(callback=callback)

        return True
