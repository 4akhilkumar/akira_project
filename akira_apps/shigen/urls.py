from django.urls import path
from . import views

urlpatterns = [
    path('resource/', views.manage_resources, name = 'manage_resources'),
    path('create_resource_save/', views.create_resource_save, name = 'create_resource_save'),
    path('view_resource/<resource_id>/', views.view_resource, name = 'view_resource'),
]