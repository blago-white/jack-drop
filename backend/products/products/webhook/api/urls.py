from django.urls import path

from .endpoints import DepositWebHookApiView


urlpatterns = [
    path("deposit/", DepositWebHookApiView.as_view(), name="deposit-web-hook")
]
