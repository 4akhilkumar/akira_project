from django.urls import path
from . import views
from .views import activate, confirm
from django.contrib.auth import views as auth_views
from akira_apps import authentication


urlpatterns = [
    path('', views.user_login, name = 'login'),
    path('logout/', views.logoutUser, name="logout"),

    path('verify_its_you/<username>/', views.verify_its_you, name="verify_its_you"),
    
    path('verify_user_by_email/<username>/', views.verify_user_by_email, name="verify_user_by_email"),
    path('confirm/<uidb64>/<token>/', confirm, name='confirm'),
    
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
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
]