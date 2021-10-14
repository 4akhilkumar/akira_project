from django.urls import path
from . import views

urlpatterns = [
    path('manage_semester/', views.manage_semester, name='manage_semester'),
    path('save_created_semester/', views.save_created_semester, name='save_created_semester'),
    path('edit_semester/<semester_id>', views.edit_semester, name='edit_semester'),
    path('save_edit_semester/<semester_id>', views.save_edit_semester, name='save_edit_semester'),
    path('delete_semester/<semester_id>', views.delete_semester, name='delete_semester'),

    path('manage_block/', views.manage_block, name='manage_block'),
    path('create_block/', views.create_block, name='create_block'),
    path('create_block_save/', views.create_block_save, name='create_block_save'),
    path('edit_block/<block_id>/', views.edit_block, name='edit_block'),
    path('edit_block_save/<block_id>/', views.edit_block_save, name='edit_block_save'),
    path('delete_block/<block_id>/', views.delete_block, name='delete_block'),

    path('manage_section_room/', views.manage_section_room, name='manage_section_room'),
    path('create_section_room/', views.create_section_room, name='create_section_room'),
    path('create_section_room_save/', views.create_section_room_save, name='create_section_room_save'),
    path('edit_section_room/<section_room_id>/', views.edit_section_room, name='edit_section_room'),
    path('edit_section_room_save/<section_room_id>/', views.edit_section_room_save, name='edit_section_room_save'),
    path('delete_section_room/<section_room_id>/', views.delete_section_room, name='delete_section_room'),

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