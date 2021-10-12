from django.urls import path
from . import views

urlpatterns = [
    path('create_semester/', views.create_semester, name='create_semester'),
    path('save_created_semester/', views.save_created_semester, name='save_created_semester'),
]