from django.urls import path
from . import views

urlpatterns = [
    path('shortURL/', views.shortURL, name="shortURL"),
    path('createShortURLAjax/', views.createShortURLAjax, name="createShortURLAjax"),
    path('akira/<str:short_url>', views.shortenURL, name="shortenURL"),
]