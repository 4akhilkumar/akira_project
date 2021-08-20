from django.urls import path
from . import views

urlpatterns = [
    path('', views.super_admin_dashboard, name = 'super_admin_dashboard'),
    path('add_staff/', views.add_staff, name="add_staff"),
    path('manage_staff/', views.manage_staff, name="manage_staff"),
    path('view_staff/<staff_id>/', views.view_staff, name="view_staff"),
]