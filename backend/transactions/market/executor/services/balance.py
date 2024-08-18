import aiohttp
import dataclasses

from rest_framework.exceptions import APIException
from django.conf import settings

import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from common.services.base import BaseMarketApiService

from executor.services.wallet import TronWalletApiService


@dataclasses.dataclass
class PaymentDetails:
    address: str
    rate: float
    amount_rub: float
    amount_trx: float


class _BotPaymentsService:
    __driver: webdriver = None

    _password: str
    _login: str

    def __init__(self):
        self._password = settings.MARKET_BOT_PASSWORD
        self._login = settings.MARKET_BOT_LOGIN
        self._market_login_url = settings.MARKET_LOGIN_URL

    @property
    def _driver(self):
        if not self.__driver:
            chrome_options = Options()

            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')

            self.__driver = webdriver.Chrome(options=chrome_options)

        return self.__driver

    async def create(self, amount: float):
        self._authenticate()
        payment = await self._init_payment(amount=amount)

        return payment

    def _authenticate(self):
        self._pass_login_form()
        self._select_account()

    async def _init_payment(self, amount: float) -> PaymentDetails:
        self._driver.get(
            f"https://rust.tm/checkin/pay/{amount}/tron/?currency=RUB"
        )

        WebDriverWait(self._driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "address_val"),
            )
        )

        token = self._driver.current_url.split("?token=")[-1]

        transaction_data = await self._get_payment_details(token=token)

        if not transaction_data:
            raise APIException("Error retrieve payment details!")

        transaction_data = transaction_data.get("data")

        return PaymentDetails(
            address=transaction_data.get("address"),
            amount_trx=round(float(
                transaction_data.get("initial_amount")
            ) / float(
                transaction_data.get("rate")
            ), 2),
            amount_rub=float(
                transaction_data.get("initial_amount")
            ),
            rate=float(
                transaction_data.get("rate")
            )
        )

    def _select_account(self):
        WebDriverWait(self._driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH,
                 "/html/body/div[1]/div[7]/div[4]/div/div[2]/div[2]/div/form/input[5]"),
            )
        )

        throught_submit = self._driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[7]/div[4]/div/div[2]/div[2]/div/form/input[5]"
        )

        throught_submit.click()

    def _pass_login_form(self):
        self._driver.get(self._market_login_url)

        WebDriverWait(self._driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "_2GBWeup5cttgbTw8FM3tfx"),
            ),
            expected_conditions.presence_of_element_located(
                (By.XPATH,
                 "/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input"),
            )
        )

        username = self._driver.find_element(
            By.CLASS_NAME,
            "_2GBWeup5cttgbTw8FM3tfx"
        )
        password = self._driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input"
        )
        submit = self._driver.find_element(
            By.CLASS_NAME,
            "DjSvCZoKKfoNSmarsEcTS"
        )

        username.send_keys(self._login)
        password.send_keys(self._password)

        submit.click()

    async def _get_payment_details(self, token: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://invoice.guide/api/get?token={token}"
            ) as response:
                if not response.ok:
                    return False

                return await response.json()


class ApiBotBalanceService(BaseMarketApiService):
    def __init__(
            self,
            *args,
            payment_service: _BotPaymentsService = _BotPaymentsService(),
            wallet_service: TronWalletApiService = TronWalletApiService(),
            **kwargs
    ):
        self._payment_service = payment_service
        self._wallet_service = wallet_service

        super().__init__(*args, **kwargs)

    async def get_current(self) -> float:
        async with (aiohttp.ClientSession() as session):
            async with session.post(
                    url=settings.BALANCE_MARKET_ENDPOINT_URL.format(
                        apikey=self._apikey,
                    )
            ) as response:
                result = await response.json()

        if not result.get("success"):
            return 0.0

        return result.get("money")

    async def replenish(self, amount: float):
        payment = await self._payment_service.create(amount=amount)

        await self._wallet_service.pay(
            amount=payment.amount_trx,
            to=payment.address
        )
