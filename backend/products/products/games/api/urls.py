from django.urls import path

from .endpoints import DropItemGameApiView

urlpatterns = [
    path("drop/<int:case_id>/", DropItemGameApiView.as_view(), name="drop"),
    # path("upgrade/"),
    # path("contract/")
]
