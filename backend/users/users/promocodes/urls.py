from django.urls import path

from .api.endpoints import UserDiscountView

urlpatterns = [
    path("api/v1/p/get_discount/", UserDiscountView.as_view())
]
