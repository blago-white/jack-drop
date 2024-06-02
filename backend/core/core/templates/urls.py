from django.urls import path

from .views import test_base_view


urlpatterns = [
    path("", test_base_view)
]
