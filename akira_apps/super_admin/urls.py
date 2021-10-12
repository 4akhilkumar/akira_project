from django.urls import path
from . import views

urlpatterns = [
    path('', views.super_admin_dashboard, name = 'super_admin_dashboard'),
    path('my_profile/', views.my_profile, name = 'my_profile'),
    path('save_my_profile/', views.save_my_profile, name = 'save_my_profile'),
    path('assign_group/', views.assign_group, name = 'assign_group'),
    path('add_staff/', views.add_staff, name = 'add_staff'),
    path('manage_staff/', views.manage_staff, name = 'manage_staff'),
    path('view_staff/<staff_id>/', views.view_staff, name = 'view_staff'),
    path('user_group/<staff_id>/', views.user_group, name = 'user_group'),
]