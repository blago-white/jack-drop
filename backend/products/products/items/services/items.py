import requests

from market.services.market import AbstractMarketAPIKeyService, MarketAPIKeyService
from items.config import MAIN_RETRIEVE_ITEM_URL

from items.items import ItemMarketParams, ItemInfo


class MarketItemParser:
    _retrieve_url: str
    _api_key_service: AbstractMarketAPIKeyService
    _market_params_dataclass: ItemMarketParams
    item_info_dataclass: ItemInfo

    def __init__(
            self, retrieve_url: str = MAIN_RETRIEVE_ITEM_URL,
            api_key_service: AbstractMarketAPIKeyService =
            MarketAPIKeyService(),
            market_params_dataclass: ItemMarketParams = ItemMarketParams,
            item_info_dataclass: ItemInfo = ItemInfo
    ):
        self._retrieve_url = retrieve_url
        self._api_key_service = api_key_service
        self._market_params_dataclass = market_params_dataclass
        self._item_info_dataclass = item_info_dataclass

    def get_info(self, url: str) -> dict:
        item_params = self._extract_item_params(crud_url=url)

        response = requests.get(
            url=self._complete_info_api_request(item_params=item_params),
            params=dict(key=self._api_key_service.apikey)
        )

        return self._parse_json_result(json=response.json())

    def _parse_json_result(self, json: dict) -> ItemInfo:
        return self._item_info_dataclass(
            title=json.get("market_name"),
            image_path="https://cdn.rust.tm/item/Skull/300.png",
            price=float(json.get("min_price"))
        )

    def _complete_info_api_request(self, item_params: ItemMarketParams) -> str:
        return self._retrieve_url.format(
            classid=item_params.classid,
            instanceid=item_params.instanceid
        )

    def _extract_item_params(self, crud_url: str) -> ItemMarketParams:
        classid, instanceid, _ = crud_url.split("/")[-2].split("-")

        return self._market_params_dataclass(
            classid=classid,
            instanceid=instanceid
        )
