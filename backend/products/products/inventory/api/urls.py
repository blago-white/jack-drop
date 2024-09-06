from django.urls import path

from .endpoints import (InventoryItemsListApiView,
                        ContractInventoryItemsListApiView,
                        UpgradeInventoryItemsListApiView,
                        UnlockInventoryItemsListApiView,
                        SellInventoryItemApiView,
                        SellAllItemsApiView,
                        WithdrawInventoryItemApiView,
                        CountInventoryItemsApiView,
                        WithdrawedItemsApiView)

urlpatterns = [
    path("all/",
         InventoryItemsListApiView.as_view(),
         name="inventory-all"),
    path("unlock/",
         UnlockInventoryItemsListApiView.as_view(),
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
    path("sell/all/", SellAllItemsApiView.as_view(), name="sell-all-items"),
    path("count/",
         CountInventoryItemsApiView.as_view(),
         name="count-inventory-items"),
    path("withdraw/<int:item_id>/",
         WithdrawInventoryItemApiView.as_view(),
         name="withdraw-item"),
    path("withdrawed/",
         WithdrawedItemsApiView.as_view(),
         name="withdrawed-callback")
]
