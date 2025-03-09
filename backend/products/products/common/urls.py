"""
URL configuration for common project.

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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, path, include

urlpatterns = [
    path(os.environ.get("ADMIN_PANEL_URL"), admin.site.urls),
    path('products/cases/', include("cases.urls")),
    path('products/items/', include("items.urls")),
    path('products/games/', include("games.urls")),
    path('products/lottery/', include("lottery.urls")),
    path('products/inventory/', include("inventory.urls")),
    path('products/bonus-buy/', include("bonus.urls")),
    path('products/private/webhook/', include("webhook.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^i18n/', include('django.conf.urls.i18n'))]
