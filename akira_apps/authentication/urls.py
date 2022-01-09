from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.user_login, name = 'login'),
    path('logout/', views.logoutUser, name="logout"),

    path('verify_its_you/<username>/', views.verify_its_you, name="verify_its_you"),

    path('secure_account/<username>/<user_response>/', views.secure_account, name="secure_account"),

    path('confirmUserLogin/<username>/', views.confirmUserLogin, name="confirmUserLogin"),

    path('checkUserResponse/<username>/', views.checkUserResponse, name="checkUserResponse"),
    
    path('verify_user_by_email/<username>/', views.verify_user_by_email, name="verify_user_by_email"),
    path('verify_user_by_backup_codes/<username>/', views.verify_user_by_backup_codes, name="verify_user_by_backup_codes"),
    path('confirm/<uidb64>/<token>/', views.confirm, name='confirm'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('twofa_verify_its_you/<username>/', views.twofa_verify_its_you, name="twofa_verify_its_you"),
    # path('twofa_verify_user_by_email/<username>/', views.twofa_verify_user_by_email, name="twofa_verify_user_by_email"),
    # path('twofacauth_email/<uidb64>/<token>/', views.twofacauth_email, name='twofacauth_email'),
    # path('confirm2FAEmailStatus/<username>/', views.confirm2FAEmailStatus, name="confirm2FAEmailStatus"),
    path('twofa_verify_user_by_backup_codes/<username>/', views.twofa_verify_user_by_backup_codes, name="twofa_verify_user_by_backup_codes"),
    
    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="authentication/password_reset/password_reset.html", 
                                            html_email_template_name = 'authentication/password_reset/password_reset_email.html',
                                            subject_template_name = 'authentication/password_reset/password_reset_subject.txt'),
        name="reset_password"),
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="authentication/password_reset/password_reset_sent.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset/password_reset_form.html"),
        name="password_reset_confirm"),
    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="authentication/password_reset/password_reset_complete.html"),
        name="password_reset_complete"),

    path('requestSwitchDevice/', views.requestSwitchDevice, name="requestSwitchDevice"),
    path('validateSwitchDevice/', views.validateSwitchDevice, name="validateSwitchDevice"),
    path('checkValidatedSwitchDeviceRequest/<username>/', views.checkValidatedSwitchDeviceRequest, name="checkValidatedSwitchDeviceRequest"),
    path('SwitchDeviceStatus/<username>/', views.SwitchDeviceStatus, name="SwitchDeviceStatus"),
    path('SyncDevice/', views.SyncDevice, name="SyncDevice"),
]