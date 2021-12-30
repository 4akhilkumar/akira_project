from django.urls import path
from . import views

urlpatterns = [
    path('manage_specializations/', views.manage_specializations, name='manage_specializations'),
    path('create_specialization_save/', views.create_specialization_save, name='create_specialization_save'),
    path('view_specialization/<specialization_name>/', views.view_specialization, name='view_specialization'),
    path('search_specialization/', views.search_specialization, name='search_specialization'),
    path('delete_specialization/<specialization_id>/', views.delete_specialization, name='delete_specialization'),
]