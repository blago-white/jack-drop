from django.urls import path

from .endpoints import ReferalStatusRetrieveAPIView, AddReferrApiView, AddLoseFundsApiView

urlpatterns = [
    path("api/v1/public/status/",
         ReferalStatusRetrieveAPIView.as_view()),
    path("api/v1/p/add-lose/",
         AddLoseFundsApiView.as_view()),
]
