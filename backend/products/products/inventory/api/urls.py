from django.urls import path

from .endpoints import InventoryItemsListApiView


urlpatterns = [
    path("all/", InventoryItemsListApiView.as_view(), name="inventory-all")
]
