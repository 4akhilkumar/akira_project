"""akira URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('akira_apps.authentication.urls')),
    path('admin/', include('akira_apps.super_admin.urls')),
    path('staff/', include('akira_apps.staff.urls')),
    path('student/', include('akira_apps.student.urls')),
    path('academicRegistration/', include('akira_apps.academic_registration.urls')),
    path('academic/', include('akira_apps.academic.urls')),
    path('accounts/', include('akira_apps.accounts.urls')),
    path('course/', include('akira_apps.course.urls')),
    path('shigen/', include('akira_apps.shigen.urls')),
    path('adops/', include('akira_apps.adops.urls')),
    path('', include('akira_apps.URLShortener.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)