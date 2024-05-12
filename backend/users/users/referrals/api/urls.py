from django.urls import path

from .endpoints import ReferalStatusRetrieveAPIView

urlpatterns = [
    path("api/v1/status/<int:referr_id>/", ReferalStatusRetrieveAPIView.as_view())
]
