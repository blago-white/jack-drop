from django.urls import path

from .api.endpoints import PromocodeDiscountView

urlpatterns = [
    path("api/v1/p/get_discount/", PromocodeDiscountView.as_view())
]
