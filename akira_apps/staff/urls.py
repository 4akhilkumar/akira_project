from django.urls import path
from . import views

urlpatterns = [
    path('staff_dashboard/', views.staff_dashboard, name="staff_dashboard"),
    path('cc_dashboard/', views.cc_dashboard, name="cc_dashboard"),
    path('hod_dashboard/', views.hod_dashboard, name="hod_dashboard"),
    path('create_courses/', views.create_courses, name="create_courses"),
    path('update_courses/', views.update_courses, name="update_courses"),
    path('delete_courses/', views.delete_courses, name="delete_courses"),
    path('manage_courses/', views.manage_courses, name="manage_courses"),
    path('view_course/<course_id>/', views.view_courses, name="view_course"),
]