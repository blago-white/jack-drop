from django.urls import path

from .endpoints import ItemsListApiView

urlpatterns = [
    path("all/",
         ItemsListApiView.as_view(),
         name="items-list")
]
