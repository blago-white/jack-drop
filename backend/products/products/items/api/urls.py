from django.urls import path

from .endpoints import ItemsListApiView, ItemsSetsListApiView

urlpatterns = [
    path("all/",
         ItemsListApiView.as_view(),
         name="items-list"),
    path("sets/",
         ItemsSetsListApiView.as_view(),
         name="items-sets")
]
