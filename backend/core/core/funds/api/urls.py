from django.urls import path

from .endpoints import (DecreaseDinamicFundsApiView,
                        IncreaseDinamicFundsApiView,
                        RetrieveDinamicFundsApiView)

urlpatterns = [
    path("increase/", IncreaseDinamicFundsApiView.as_view(),
         name="increase"),
    path("decrease/", DecreaseDinamicFundsApiView.as_view(),
         name="decrease"),
    path("get-displayed/", RetrieveDinamicFundsApiView.as_view(),
         name="get-displayed")
]
