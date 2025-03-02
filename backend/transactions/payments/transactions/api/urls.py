from django.urls import path

from .endpoints import NicepayInitReplenishApiView, NicePayTransactionCallbackApiView, \
    TransactionValidationApiView

urlpatterns = [
    path("create/", NicepayInitReplenishApiView.as_view(), name="init"),
    path("callback/", NicePayTransactionCallbackApiView.as_view(), name="callback"),
    path("callback-skinify/"),
    path("validate/", TransactionValidationApiView.as_view(), name="validate"),
]
