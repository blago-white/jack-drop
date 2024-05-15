from django.urls import path

from .endpoints import ReferalStatusRetrieveAPIView, AddReferrApiView

urlpatterns = [
    path("api/v1/p/status/<int:referr_id>/",
         ReferalStatusRetrieveAPIView.as_view()),
    path("api/v1/add_referr/",
         AddReferrApiView.as_view())
]
