from django.urls import path

from .endpoints import DropCaseItemApiView

urlpatterns = [
    path("drop/",
         DropCaseItemApiView.as_view(),
         name="drop-item-view")
]