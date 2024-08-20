from django.urls import path

from .endpoints import InitReplenishApiView, TransactionCallbackApiView

urlpatterns = [
    path("create/", InitReplenishApiView.as_view(), name="init"),
    path("callback/", TransactionCallbackApiView.as_view(), name="callback"),
]
