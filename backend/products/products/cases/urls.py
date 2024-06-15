from django.urls import path

from .apiviews.cases import CasesListAPIView, CaseRetrieveAPIView
from .apiviews.items import CaseItemsListAPIView
from .views.cases import CasesView
from .views.categories import CasesCategoriesView
from .api import urls

urlpatterns = [
    path("api/v1/cases/", CasesListAPIView.as_view()),
    path("api/v1/case/<int:case_pk>/items/", CaseItemsListAPIView.as_view()),
    path("api/v1/case/<int:case_pk>/", CaseRetrieveAPIView.as_view()),
    path("cases/", CasesCategoriesView.as_view())
]
