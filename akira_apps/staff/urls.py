from django.urls import path
from . import views

urlpatterns = [
    path('add_staff/', views.add_staff, name = 'add_staff'),
    path('bulk_upload_staffs_save/', views.bulk_upload_staffs_save, name = 'bulk_upload_staffs_save'),

    path('applicant_dashboard/', views.applicant_dashboard, name="applicant_dashboard"),
    path('teachingstaff_dashboard/', views.teachingstaff_dashboard, name="teachingstaff_dashboard"),
    path('adops_dashboard/', views.adops_dashboard, name="adops_dashboard"),

    path('view_staff/<staff_username>/', views.view_staff, name = 'view_staff'),
    path('edit_staff/<staff_username>/', views.edit_staff, name = 'edit_staff'),

    path('staff_info_csv/', views.staff_info_csv, name = 'staff_info_csv'),
]