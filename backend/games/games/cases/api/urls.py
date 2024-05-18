from django.urls import path

from .endpoints import DropCaseItemApiView

urlpatterns = [
    path("drop/<int:case_id>/",
         DropCaseItemApiView.as_view(),
         name="drop-item-view")
]