from django.urls import path
from . import views

urlpatterns = [
    path('account_settings/', views.account_settings, name='account_settings'),
    path('generate_backup_codes/', views.generate_backup_codes, name='generate_backup_codes'),
    path('download_backup_codes/', views.download_backup_codes, name='download_backup_codes'),
    path('delete_existing_backup_codes/', views.delete_existing_backup_codes, name='delete_existing_backup_codes'),
    path('status_2fa/', views.status_2fa, name='status_2fa'),
    path('agree_login_attempt/<login_attempt_id>', views.agree_login_attempt, name='agree_login_attempt'),
    path('deny_login_attempt/<login_attempt_id>', views.deny_login_attempt, name='deny_login_attempt'),
]