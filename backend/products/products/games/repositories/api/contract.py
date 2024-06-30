from rest_framework.exceptions import APIException
from rest_framework.serializers import Serializer

from games.api.services.contract import ContractApiService
from games.api.services.site import SiteFundsApiService
from games.serializers.contract import GrantedInventoryItemsSerializer
from inventory.services.inventory import InventoryService
from items.models.models import Item
from items.serializers import ItemSerializer
from items.services.items import ItemService
from .base import BaseApiRepository


class ContractApiRepository(BaseApiRepository):
    default_inventory_service = InventoryService()
    default_items_service = ItemService()
    default_api_service = ContractApiService()
    default_site_funds_service = SiteFundsApiService()

    default_seriaizer_class = GrantedInventoryItemsSerializer
    default_item_serializer_class = ItemSerializer

    _seriaizer_class: GrantedInventoryItemsSerializer
    _api_service: ContractApiService
    _site_funds_service: SiteFundsApiService

    def __init__(self, *args,
                 seriaizer_class: GrantedInventoryItemsSerializer = None,
                 inventory_service: InventoryService = None,
                 site_funds_service: SiteFundsApiService = None,
                 items_service: ItemService = None,
                 item_serializer_class: ItemSerializer = None,
                 **kwargs):
        self._inventory_service = inventory_service or self.default_inventory_service
        self._seriaizer_class = seriaizer_class or self.default_seriaizer_class
        self._items_service = items_service or self.default_items_service
        self._item_serializer_class = item_serializer_class or self.default_item_serializer_class
        self._site_funds_service = site_funds_service or self.default_site_funds_service

        super().__init__(*args, **kwargs)

    def make_contract(self, request_data: dict, user_data: dict) -> dict:
        print(request_data, "RRRRRRRRRRRRRR")

        serialized: Serializer = self._seriaizer_class(
            data=request_data
        )

        serialized.is_valid(raise_exception=True)

        granted_amount, shifted_amount = self._get_shifted_amount(
            request_data=serialized.data,
            user_id=user_data.get("id")
        )

        contract_item: Item = self._items_service.get_closest_by_price(
            price=shifted_amount
        )

        self._commit_result(user_id=user_data.get("id"),
                            granted_items_ids=serialized.data.get(
                                "granted_inventory_items"
                            ),
                            granted_amount=granted_amount,
                            result_item=contract_item)

        self._save_contract(serializer_data={
            "user_id": user_data.get("id"),
            "granted_amount": granted_amount,
            "result_item": contract_item.pk
        })

        return self._item_serializer_class(instance=contract_item).data

    def _commit_result(self, user_id: int,
                       granted_items_ids: list[int],
                       granted_amount: float,
                       result_item: Item):
        delete = self._inventory_service.bulk_remove_from_inventory(
            owner_id=user_id,
            inventory_items_ids=granted_items_ids
        )

        if not delete:
            raise APIException("Error with inventory")

        received = self._inventory_service.add_item(
            owner_id=user_id,
            item_id=result_item.pk
        )

        self._site_funds_service.update(
            amount=granted_amount - result_item.price
        )

        return received

    def _get_shifted_amount(self, request_data: dict,
                            user_id: int) -> tuple[float, float]:
        items = request_data.get("granted_inventory_items")

        request_amount = self._inventory_service.bulk_get_items_amount(
            owner_id=user_id,
            inventory_items_ids=items
        )

        print("ITREMS", items)

        return request_amount, self._api_service.get_shifted_amount(
            amount=request_amount
        )

    def _save_contract(self, serializer_data: dict) -> None:
        success = self._api_service.save_contract(
            serialized=self._api_service.default_endpoint_serializer_class(
                instance=serializer_data,
            )
        )

        if not success:
            raise APIException("Cannot complete contract", code=404)
