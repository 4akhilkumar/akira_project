from django.urls import path
from . import views

urlpatterns = [
    path('manage_adops/', views.manage_adops, name='manage_adops'),

    path('add_openings/', views.add_openings, name='add_openings'),
    path('editOpening/<str:openingID>/', views.editOpening, name='editOpening'),
    path('deleteOpening/<str:openingID>/', views.deleteOpening, name='deleteOpening'),
    path('openings/', views.openings, name='openings'),
    path('fetch_each_opening_Ajax/', views.fetch_each_opening_Ajax, name='fetch_each_opening_Ajax'),
    path('manageOpenings/', views.manageOpenings, name='manageOpenings'),

    path('applicantsAccount/', views.applicantsAccount, name='applicantsAccount'),
    path('send_applicant_reg_email_again/<username>/', views.send_applicant_reg_email_again, name = 'send_applicant_reg_email_again'),
    path('confirm_applicant_email/<uidb64>/<token>/', views.confirm_applicant_email, name='confirm_applicant_email'),

    path('userAppliedOpenings/', views.userAppliedOpenings, name='userAppliedOpenings'),
    path('withdrawAppl/<str:openingID>/', views.withdrawAppl, name='withdrawAppl'),
    path('applicantsInfo/<str:openingID>/', views.applicantsInfo, name='applicantsInfo'),

    path('profile/', views.profile, name='profile'),

    path('createProgramme/', views.createProgramme, name='createProgramme'),
    path('editProgramme/<uuid:programmeID>/', views.editProgramme, name='editProgramme'),
    path('deleteProgramme/<uuid:programmeID>/', views.deleteProgramme, name='deleteProgramme'),
    path('manageProgrammes/', views.manageProgrammes, name='manageProgrammes'),
    path('viewProgrammes/', views.viewProgrammes, name='viewProgrammes'),

    path('createAdmission/', views.createAdmission, name='createAdmission'),
    path('manageAdmission/', views.manageAdmission, name='manageAdmission'),
    path('AdmissionbyBatch/<uuid:batchID>/', views.AdmissionbyBatch, name='AdmissionbyBatch'),
    path('acceptAdmissionAjax/', views.acceptAdmissionAjax, name='acceptAdmissionAjax'),

    path('stuAdmRegistration/', views.stuAdmRegistration, name='stuAdmRegistration'),
    path('confirm_admission_email/<uidb64>/<token>/', views.confirm_admission_email, name='confirm_admission_email'),
    path('send_stuAdm_reg_email/<EnUsername>/', views.send_stuAdm_reg_email, name = 'send_stuAdm_reg_email'),
    path('waitingStuAdmConfirmation/<str:EnUsername>/', views.waitingStuAdmConfirmation, name = 'waitingStuAdmConfirmation'),
    path('isStuAdmRegConfirmed/', views.isStuAdmRegConfirmed, name = 'isStuAdmRegConfirmed'),
    
    path('admstudent_dashboard/', views.admstudent_dashboard, name = 'admstudent_dashboard'),
]