from django.urls import path

from .endpoints import (InventoryItemsListApiView,
                        ContractInventoryItemsListApiView,
                        UpgradeInventoryItemsListApiView,
                        SellInventoryItemApiView,
                        WithdrawInventoryItemApiView,
                        CountInventoryItemsApiView)


urlpatterns = [
    path("all/",
         InventoryItemsListApiView.as_view(),
         name="inventory-all"),
    path("unlock/",
         UpgradeInventoryItemsListApiView.as_view(),
         name="inventory-upgrade"),
    path("upgrade/",
         UpgradeInventoryItemsListApiView.as_view(),
         name="inventory-upgrade"),
    path("contract/",
         ContractInventoryItemsListApiView.as_view(),
         name="inventory-contract"),
    path("sell/",
         SellInventoryItemApiView.as_view(),
         name="sell-item"),
    path("withdraw/",
         WithdrawInventoryItemApiView.as_view(),
         name="withdraw-item"),
    path("count/",
         CountInventoryItemsApiView.as_view(),
         name="count-inventory-items")
]
