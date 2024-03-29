from django.urls import path

from .views.views import CasesListAPIView


urlpatterns = [
    path("api/v1/cases/", CasesListAPIView.as_view())
]

