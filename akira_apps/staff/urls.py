from django.urls import path
from . import views

urlpatterns = [
    path('hod_dashboard/', views.hod_dashboard, name="hod_dashboard"),
    path('staff_dashboard/', views.staff_dashboard, name="staff_dashboard"),
    path('applicant_dashboard/', views.applicant_dashboard, name="applicant_dashboard"),
    path('manage_staff/', views.manage_staff, name = 'manage_staff'),
    path('bulk_upload_staffs_save/', views.bulk_upload_staffs_save, name = 'bulk_upload_staffs_save'),
    path('staff_info_csv/', views.staff_info_csv, name = 'staff_info_csv'),
    path('add_staff/', views.add_staff, name = 'add_staff'),
    path('view_staff/<staff_username>/', views.view_staff, name = 'view_staff'),
    path('edit_staff/<staff_username>/', views.edit_staff, name = 'edit_staff'),
    
    path('staff_enroll_course/<course_id>/', views.staff_enroll_course, name="staff_enroll_course"),
    path('staff_unenroll_course/<staff_enroll_course_id>/', views.staff_unenroll_course, name="staff_unenroll_course"),

    path('student_enroll_course/<course_id>/', views.student_enroll_course, name="student_enroll_course"),

    path('add_student/', views.add_student, name = 'add_student'),
]