from django.apps import AppConfig


class SuperAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'akira_apps.super_admin' # Add path i.e., akira_apps in name
