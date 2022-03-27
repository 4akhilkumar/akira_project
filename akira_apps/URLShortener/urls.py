from django.urls import path
from . import views

urlpatterns = [
    path('shortURL/', views.shortURL, name="shortURL"),
    path('akira/<str:short_url>', views.shortenURL, name="shortenURL"),
]