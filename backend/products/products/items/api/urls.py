from django.urls import path

from .endpoints import ItemsListApiView, ItemsSetsListApiView, ItemSetDetailedApiView, ItemSetBuyApiView

urlpatterns = [
    path("all/",
         ItemsListApiView.as_view(),
         name="items-list"),
    path("sets/",
         ItemsSetsListApiView.as_view(),
         name="items-sets"),
    path("set/<int:set_id>/",
         ItemSetDetailedApiView.as_view(),
         name="items-set"),
    path("set/<int:set_id>/buy/",
         ItemSetBuyApiView.as_view(),
         name="items-set-buy")
]
