from django.urls import path
from . import views

urlpatterns = [
    path('adminInstituteRegistration/', views.adminInstituteRegistration, name = 'adminInstituteRegistration'),
    path('confirm_admin_email/<uidb64>/<token>/', views.confirm_admin_email, name='confirm_admin_email'),
    path('super_admin_dashboard/', views.super_admin_dashboard, name = 'super_admin_dashboard'),
    path('my_profile/', views.my_profile, name = 'my_profile'),
    path('save_my_profile/', views.save_my_profile, name = 'save_my_profile'),
    path('assign_group/', views.assign_group, name = 'assign_group'),
    path('assign_user_group/<staff_username>/', views.assign_user_group, name = 'assign_user_group'),
    path('send_admin_reg_email_again/<username>/', views.send_admin_reg_email_again, name = 'send_admin_reg_email_again'),
]