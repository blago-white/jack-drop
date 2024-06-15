from django.urls import path

from .views import test_ws_view

urlpatterns = [
    path("test/<int:k>/", test_ws_view)
]
