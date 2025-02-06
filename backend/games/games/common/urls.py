"""
URL configuration for games project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(os.environ.get("ADMIN_PANEL_URL"), admin.site.urls),
    path('games/private/case/', include("cases.urls")),
    path('games/private/upgrade/', include("upgrade.urls")),
    path('games/private/contract/', include("contract.urls")),
    path('games/private/battle/', include("battles.urls")),
    path('games/private/mines/', include("mines.urls")),
    path('games/private/fortune/', include("fortune.urls")),
]
