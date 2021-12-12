from django.urls import path
from . import views

urlpatterns = [
    path('hod_dashboard/', views.hod_dashboard, name="hod_dashboard"),
    path('staff_dashboard/', views.staff_dashboard, name="staff_dashboard"),
    
    path('staff_enroll_course/<course_id>/', views.staff_enroll_course, name="staff_enroll_course"),
    path('staff_unenroll_course/<staff_enroll_course_id>/', views.staff_unenroll_course, name="staff_unenroll_course"),

    path('student_enroll_course/<course_id>/', views.student_enroll_course, name="student_enroll_course"),

    path('add_student/', views.add_student, name = 'add_student'),
]