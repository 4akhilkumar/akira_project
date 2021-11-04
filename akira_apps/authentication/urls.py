from django.urls import path
from . import views
from .views import activate
from django.contrib.auth import views as auth_views
from akira_apps import authentication


urlpatterns = [
    path('', views.user_login, name = 'login'),
    path('logout/', views.logoutUser, name="logout"),
    
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]