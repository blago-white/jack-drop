import math

import requests

from items.config import (MAIN_RETRIEVE_ITEM_URL,
                          BULK_RETRIEVE_ITEMS_URL,
                          MAIN_RETRIEVE_ITEM_IMAGE_URL)
from market.items import ItemMarketParams, ItemInfo
from market.services.market import AbstractMarketAPIKeyService, \
    MarketAPIKeyService


class MarketItemParser:
    _retrieve_url: str
    _mass_retrieve_url: str

    _api_key_service: AbstractMarketAPIKeyService
    _market_params_dataclass: ItemMarketParams
    item_info_dataclass: ItemInfo

    def __init__(
            self, retrieve_url: str = MAIN_RETRIEVE_ITEM_URL,
            mass_retrieve_url: str = BULK_RETRIEVE_ITEMS_URL,
            api_key_service: AbstractMarketAPIKeyService =
            MarketAPIKeyService(),
            market_params_dataclass: ItemMarketParams = ItemMarketParams,
            item_info_dataclass: ItemInfo = ItemInfo
    ):
        self._retrieve_url = retrieve_url
        self._api_key_service = api_key_service
        self._market_params_dataclass = market_params_dataclass
        self._item_info_dataclass = item_info_dataclass
        self._mass_retrieve_url = mass_retrieve_url

    def bulk_get_prices(self, market_items_links: list[str]) -> list[float]:
        total = []

        for batch in range(50, len(market_items_links)+50, 50):
            batch_prices = self._bulk_get_prices(
                list_=",".join([
                    self._extract_item_params_crud(i)
                    for i in market_items_links[batch-50:batch]
                ])
            )

            total.extend(batch_prices)

        return total

    def _bulk_get_prices(self, list_: str) -> list[float]:
        response = requests.post(
            url=self._mass_retrieve_url.format(self._api_key_service.apikey),
            data=dict(list=list_)
        )

        result = response.json()

        if (not response.ok) or (not result.get("success")):
            raise Exception("Cannot retrieve prices")

        results: list[dict[str, str | dict]] = result.get("results")

        prices = []

        for i in results:
            price = float(
                i.get("sell_offers").get("best_offer", 0)
            ) / 100

            price = min(price + 100, price*1.05)

            prices.append(round(price, 2))

        return [max(p, 0) for p in prices]

    def get_info(self, url: str) -> ItemInfo:
        item_params = self._extract_item_params(crud_url=url)

        response = requests.get(
            url=self._complete_info_api_request(item_params=item_params),
            params=dict(key=self._api_key_service.apikey)
        )

        return self._parse_json_result(json=response.json())

    def _parse_json_result(self, json: dict) -> ItemInfo:
        price = float(json.get("min_price"))//100
        price = round(min(price + 100, price*1.05), 2)

        return self._item_info_dataclass(
            title=json.get("market_name"),
            image_path=self._get_item_image_path(
                json.get("market_name")
            ),
            price=price,
            market_hash_name=json.get("market_hash_name")
        )

    def _complete_info_api_request(self, item_params: ItemMarketParams) -> str:
        return self._retrieve_url.format(
            classid=item_params.classid,
            instanceid=item_params.instanceid
        )

    def _extract_item_params(self, crud_url: str) -> ItemMarketParams:
        classid, instanceid, *_ = crud_url.split("/")[-2].split("-")

        return self._market_params_dataclass(
            classid=classid,
            instanceid=instanceid
        )

    @staticmethod
    def _extract_item_params_crud(crud_url: str) -> ItemMarketParams:
        classid, instanceid, *_ = crud_url.split("/")[-2].split("-")

        return f"{classid}_{instanceid}"

    @staticmethod
    def _get_item_image_path(item_name: str) -> str:
        item_name = item_name.replace(" ", "+")

        return MAIN_RETRIEVE_ITEM_IMAGE_URL.format(name=item_name)
