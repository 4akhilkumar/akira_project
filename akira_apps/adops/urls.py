from django.urls import path
from . import views

urlpatterns = [
    path('manage_adops/', views.manage_adops, name='manage_adops'),
    path('add_openings/', views.add_openings, name='add_openings'),
    path('editOpening/<str:openingID>/', views.editOpening, name='editOpening'),
    path('deleteOpening/<str:openingID>/', views.deleteOpening, name='deleteOpening'),
    path('userAppliedOpenings/', views.userAppliedOpenings, name='userAppliedOpenings'),
    path('withdrawAppl/<str:openingID>/', views.withdrawAppl, name='withdrawAppl'),
    path('applicantsInfo/<str:openingID>/', views.applicantsInfo, name='applicantsInfo'),

    path('profile/', views.profile, name='profile'),

    path('openings/', views.openings, name='openings'),

    path('applicantsAccount/', views.applicantsAccount, name='applicantsAccount'),
    path('confirm_applicant_email/<uidb64>/<token>/', views.confirm_applicant_email, name='confirm_applicant_email'),
    path('send_applicant_reg_email_again/<username>/', views.send_applicant_reg_email_again, name = 'send_applicant_reg_email_again'),

    path('fetch_each_opening_Ajax/', views.fetch_each_opening_Ajax, name='fetch_each_opening_Ajax'),
    path('fetch_each_applicant_Ajax/', views.fetch_each_applicant_Ajax, name='fetch_each_applicant_Ajax'),
    # path('draft_opening_Ajax/', views.draft_opening_Ajax, name='draft_opening_Ajax'),
]