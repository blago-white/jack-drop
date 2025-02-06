"""
URL configuration for core project.

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

print(os.environ.get("ADMIN_PANEL_URL"))

urlpatterns = [
    path(os.environ.get("ADMIN_PANEL_URL"), admin.site.urls),
    path('private/api/v1/funds/', include("funds.urls")),
    path("", include("templates.urls")),
    path('i18n/', include('django.conf.urls.i18n')),
]
