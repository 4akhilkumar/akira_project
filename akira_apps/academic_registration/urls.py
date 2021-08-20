from django.urls import path
from . import views

urlpatterns = [
    path('', views.academic_registration_dashboard, name = 'academic_registration_dashboard'),
]