from django.urls import path

from .endpoints import NicepayInitReplenishApiView, NicePayTransactionCallbackApiView, \
    TransactionValidationApiView, SkinifyTransactionCallbackApiView

urlpatterns = [
    path("create/", NicepayInitReplenishApiView.as_view(), name="init"),
    path("callback/", NicePayTransactionCallbackApiView.as_view(), name="callback-nicepay"),
    path("callback-skinify/", SkinifyTransactionCallbackApiView.as_view(), name="callback-skinify"),
    path("validate/", TransactionValidationApiView.as_view(), name="validate"),
]
