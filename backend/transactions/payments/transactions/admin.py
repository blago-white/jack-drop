from django.contrib import admin

from .models import Config, Payment

admin.site.register(Config)
admin.site.register(Payment)
