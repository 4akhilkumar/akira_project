from django.urls import path
from . import views

urlpatterns = [
    path('staff_dashboard/', views.staff_dashboard, name="staff_dashboard"),
    path('cc_dashboard/', views.cc_dashboard, name="cc_dashboard"),
    path('hod_dashboard/', views.hod_dashboard, name="hod_dashboard"),
    
    path('create_courses/', views.create_courses, name="create_courses"),
    path('save_created_course/', views.save_created_course, name="save_created_course"),
    path('edit_course/<course_id>/', views.edit_course, name="edit_course"),
    path('save_edit_course/<course_id>/', views.save_edit_course, name="save_edit_course"),
    path('delete_courses/<course_id>/', views.delete_courses, name="delete_courses"),
    path('manage_courses/', views.manage_courses, name="manage_courses"),
    path('view_course/<course_id>/', views.view_course, name="view_course"),

    path('staff_enroll_course/<course_id>/', views.staff_enroll_course, name="staff_enroll_course"),
    path('staff_unenroll_course/<staff_enroll_course_id>/', views.staff_unenroll_course, name="staff_unenroll_course"),

    path('student_enroll_course/<course_id>/', views.student_enroll_course, name="student_enroll_course"),

    path('add_student/', views.add_student, name = 'add_student'),
]