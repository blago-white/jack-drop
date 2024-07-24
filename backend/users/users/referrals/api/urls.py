from django.urls import path

from .endpoints import ReferalStatusRetrieveAPIView, AddReferrApiView

urlpatterns = [
    path("api/v1/public/status/",
         ReferalStatusRetrieveAPIView.as_view()),
]
