from django.urls import path

from .endpoints import InitReplenishApiView

urlpatterns = [
    path("create/", InitReplenishApiView.as_view(), name="init"),
]
