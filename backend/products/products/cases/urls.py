from django.urls import path

from .apiviews.cases import CasesListAPIView, CaseRetrieveAPIView, CasesByCategoriesListAPIView
from .apiviews.items import CaseItemsListAPIView
from .views.cases import CasesView
from .views.categories import CasesCategoriesView

urlpatterns = [
    path("api/v1/by-categories/", CasesByCategoriesListAPIView.as_view()),
    path("api/v1/cases/", CasesListAPIView.as_view()),
    path("api/v1/case/<int:case_pk>/items/", CaseItemsListAPIView.as_view()),
    path("api/v1/case/<int:case_pk>/", CaseRetrieveAPIView.as_view()),
]
