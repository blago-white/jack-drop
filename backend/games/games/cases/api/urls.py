from django.urls import path

from .endpoints import DropCaseItemApiView

urlpatterns = [
    path("api/v1/p/drop/",
         DropCaseItemApiView.as_view(),
         name="drop-item-view")
]