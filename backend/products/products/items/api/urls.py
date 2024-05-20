from django.urls import path
from .endpoints import ItemPriceApiView


urlpatterns = [
    path("api/v1/p/item_price/<int:item_id>/",
         ItemPriceApiView.as_view(),
         name="item-price")
]
