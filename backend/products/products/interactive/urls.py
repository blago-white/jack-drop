from django.urls import path

from .views import test_ws_view

urlpatterns = [
    path("test/", test_ws_view)
]
