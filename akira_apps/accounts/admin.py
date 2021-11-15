from django.contrib import admin

from akira_apps.accounts.models import TwoFactorAuth

# Register your models here.
admin.site.register(TwoFactorAuth)