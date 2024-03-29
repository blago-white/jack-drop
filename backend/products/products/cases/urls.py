from django.urls import path

from .views.cases import CasesListAPIView
from .views.items import CaseItemsListAPIView


urlpatterns = [
    path("api/v1/cases/", CasesListAPIView.as_view()),
    path("api/v1/case/items/<slug:case_pk>/", CaseItemsListAPIView.as_view())
]

