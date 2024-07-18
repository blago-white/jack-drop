from django.urls import path

from .api import urls
from .views import SteamAuthView, SteamAuthProcessView


urlpatterns = [
    path("", SteamAuthView.as_view(), name="login-view"),
    path("process/", SteamAuthProcessView.as_view(), name="login-callback"),
]

urlpatterns += urls.urlpatterns
