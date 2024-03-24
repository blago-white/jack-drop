from django.contrib.admin.apps import AdminConfig


class JackDropAdminConfig(AdminConfig):
    default_site = "common.admin.JackDropAdmin"
