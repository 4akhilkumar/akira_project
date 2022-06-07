from django.urls import path
from . import views

urlpatterns = [
    path('add_staff/', views.add_staff, name = 'add_staff'),
    path('bulk_upload_staffs_save/', views.bulk_upload_staffs_save, name = 'bulk_upload_staffs_save'),

    path('applicant_dashboard/', views.applicant_dashboard, name="applicant_dashboard"),
    path('teachingstaff_dashboard/', views.teachingstaff_dashboard, name="teachingstaff_dashboard"),
    path('adops_dashboard/', views.adops_dashboard, name="adops_dashboard"),

    path('viewStaff/<username>/', views.viewStaff, name = 'viewStaff'),
    path('editStaff/<username>/', views.editStaff, name = 'editStaff'),

    path('CreateDesignationAjax', views.CreateDesignationAjax, name = 'CreateDesignationAjax'),
    path('setUserDesignationAjax', views.setUserDesignationAjax, name = 'setUserDesignationAjax'),

    path('staff_info_csv/', views.staff_info_csv, name = 'staff_info_csv'),
]