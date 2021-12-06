from django.urls import path
from . import views

urlpatterns = [
    path('', views.super_admin_dashboard, name = 'super_admin_dashboard'),
    path('my_profile/', views.my_profile, name = 'my_profile'),
    path('save_my_profile/', views.save_my_profile, name = 'save_my_profile'),
    path('assign_group/', views.assign_group, name = 'assign_group'),
    path('add_staff/', views.add_staff, name = 'add_staff'),
    path('bulk_upload_staffs_save/', views.bulk_upload_staffs_save, name = 'bulk_upload_staffs_save'),
    path('staff_info_csv/', views.staff_info_csv, name = 'staff_info_csv'),
    path('manage_staff/', views.manage_staff, name = 'manage_staff'),
    path('view_staff/<staff_username>/', views.view_staff, name = 'view_staff'),
    path('edit_staff/<staff_username>/', views.edit_staff, name = 'edit_staff'),
    path('assign_user_group/<staff_username>/', views.assign_user_group, name = 'assign_user_group'),
]