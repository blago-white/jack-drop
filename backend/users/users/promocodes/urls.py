from django.urls import path

from .api.endpoints import PromocodeDiscountView, PersonalOffersView

urlpatterns = [
    path("api/v1/p/get_discount/", PromocodeDiscountView.as_view()),
    path("api/v1/public/get-offer/", PersonalOffersView.as_view())
]
