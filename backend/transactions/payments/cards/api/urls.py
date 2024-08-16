from django.urls import path

from .endpoints import CreateTransactionApiView

urlpatterns = [
    path("create/", CreateTransactionApiView.as_view(), name="create-card")
]
