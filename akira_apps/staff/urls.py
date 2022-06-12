from django.urls import path
from . import views

urlpatterns = [
    path('applicant_dashboard/', views.applicant_dashboard, name="applicant_dashboard"),
    path('teachingstaff_dashboard/', views.teachingstaff_dashboard, name="teachingstaff_dashboard"),
    path('adops_dashboard/', views.adops_dashboard, name="adops_dashboard"),

    path('bulk_upload_staffs_save/', views.bulk_upload_staffs_save, name = 'bulk_upload_staffs_save'),

    path('add_staff/', views.add_staff, name = 'add_staff'),
    path('confirm_staff_email/<uidb64>/<token>/', views.confirm_staff_email, name='confirm_staff_email'),
    path('send_staff_reg_email/<EnUsername>/', views.send_staff_reg_email, name = 'send_staff_reg_email'),
    path('waitingStaffConfirmation/<str:EnUsername>/', views.waitingStaffConfirmation, name = 'waitingStaffConfirmation'),
    path('isStaffRegConfirmed/', views.isStaffRegConfirmed, name = 'isStaffRegConfirmed'),

    path('CreateDesignationAjax', views.CreateDesignationAjax, name = 'CreateDesignationAjax'),
    path('setUserDesignationAjax', views.setUserDesignationAjax, name = 'setUserDesignationAjax'),

    path('staff_info_csv/', views.staff_info_csv, name = 'staff_info_csv'),
]