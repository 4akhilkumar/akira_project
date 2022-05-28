from django.urls import path
from . import views

urlpatterns = [
    path('createShortURLAjax/', views.createShortURLAjax, name="createShortURLAjax"),
    path('ak/<str:short_url>', views.shortenURL, name="shortenURL"),
    path('urlshortenermf/', views.urlshortenermf, name="urlshortenermf"),
    path('selectedSULogsAjax/', views.selectedSULogsAjax, name="selectedSULogsAjax"),
]