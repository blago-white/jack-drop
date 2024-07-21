from django.urls import path

from .apiviews.cases import (PaidCasesListAPIView, CasesListAPIView,
                             CaseRetrieveAPIView, CasesByCategoriesListAPIView)
from .apiviews.items import CaseItemsListAPIView

urlpatterns = [
    path("api/v1/by-categories/", CasesByCategoriesListAPIView.as_view()),
    path("api/v1/cases/", CasesListAPIView.as_view()),
    path("api/v1/paid-cases/", PaidCasesListAPIView.as_view()),
    path("api/v1/case/<int:case_pk>/items/", CaseItemsListAPIView.as_view()),
    path("api/v1/case/<int:case_pk>/", CaseRetrieveAPIView.as_view()),
]
