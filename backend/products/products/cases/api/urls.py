from django.urls import path

from .endpoints import GetCaseDataPrivateApiView

urlpatterns = [
    path("api/v1/p/case_drop_data/<int:case_id>/",
         GetCaseDataPrivateApiView.as_view())
]
