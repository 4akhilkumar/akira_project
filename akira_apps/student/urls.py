from django.urls import path
from . import views

urlpatterns = [
    path('student_dashboard/', views.student_dashboard, name = 'student_dashboard'),
    path('manage_students/', views.manage_students, name = 'manage_students'),
    path('view_student/<student_username>/', views.view_student, name = 'view_student'),
    path('bulk_upload_students_save/', views.bulk_upload_students_save, name = 'bulk_upload_students_save'),
    path('students_info_csv/', views.students_info_csv, name = 'students_info_csv'),
    path('search_student/', views.search_student, name='search_student'),
]