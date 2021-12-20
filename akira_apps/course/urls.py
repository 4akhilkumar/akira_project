from django.urls import path
from . import views

urlpatterns = [
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('create_course_save/', views.create_course_save, name='create_course_save'),
    path('view_course/<course_code>/', views.view_course, name='view_course'),
    path('search_course/', views.search_course, name='search_course'),
    path('delete_course/<course_id>/', views.delete_course, name='delete_course'),
]