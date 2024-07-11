from django.urls import path

from .endpoints import AddItemToScheduleApiView

urlpatterns = [
    path("add/", AddItemToScheduleApiView.as_view(), name="add-item-to-schedule")
]
