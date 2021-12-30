from django.urls import path
from . import views

urlpatterns = [
    path('sem_registration/', views.sem_registration, name='sem_registration'),
    path('manage_specialization/', views.manage_specialization, name='manage_specialization'),
    path('create_specialization/', views.create_specialization, name='create_specialization'),
    path('create_specialization_save/', views.create_specialization_save, name='create_specialization_save'),
    path('view_specialization/<specialization_id>/', views.view_specialization, name='view_specialization'),
    path('edit_specialization/<specialization_id>/', views.edit_specialization, name='edit_specialization'),
    path('edit_specialization_save/<specialization_id>/', views.edit_specialization_save, name='edit_specialization_save'),
    path('delete_specialization/<specialization_id>/', views.delete_specialization, name='delete_specialization'),

    path('staff_enroll_specialization/<specialization_id>/', views.staff_enroll_specialization, name="staff_enroll_specialization"),
    path('student_enroll_specialization/<specialization_id>/', views.student_enroll_specialization, name="student_enroll_specialization"),
    path('student_unenroll_specialization/<specialization_id>/', views.student_unenroll_specialization, name="student_unenroll_specialization"),
    
]