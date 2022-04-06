from django.urls import path
from . import views

urlpatterns = [
    path('sem_registration/', views.sem_registration, name='sem_registration'),
    path('enrollSpec/<uuid:speci_id>/', views.enrollSpec, name='enrollSpec'),
    path('unenrollSpec/<uuid:speci_id>/', views.unenrollSpec, name='unenrollSpec'),
    path('create_semester_save/', views.create_semester_save, name='create_semester_save'),
    path('fetch_semester/<semester_id>/', views.fetch_semester, name='fetch_semester'),
    path('update_semester_save/<semester_id>/', views.update_semester_save, name='update_semester_save'),
    path('delete_semester/<semester_id>/', views.delete_semester, name='delete_semester'),

    path('createsemesterAjax/', views.createsemesterAjax, name='createsemesterAjax'),
    path('getAllSemestersAjax/', views.getAllSemestersAjax, name='getAllSemestersAjax')
]