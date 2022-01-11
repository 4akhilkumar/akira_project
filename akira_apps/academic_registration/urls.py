from django.urls import path
from . import views

urlpatterns = [
    path('sem_registration/', views.sem_registration, name='sem_registration'),
    path('enrollSpec/<uuid:speci_id>/', views.enrollSpec, name='enrollSpec'),
    path('unenrollSpec/<uuid:speci_id>/', views.unenrollSpec, name='unenrollSpec'),
]