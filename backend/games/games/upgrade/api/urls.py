from django.urls import path

from .endpoints import UpgradeApiView

urlpatterns = [
    path("new/", UpgradeApiView.as_view(), name="make-upgrade")
]
