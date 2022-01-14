"""
Django settings for akira project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8d2)%0!b0ql!&++qg864qy3xqae$@#qlut7_39hv%&7grb1l7$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Added the created apps here with their path i.e., akira_apps
    'akira_apps.super_admin.apps.SuperAdminConfig',
    'akira_apps.staff.apps.StaffConfig',
    'akira_apps.student.apps.StudentConfig',
    'akira_apps.authentication.apps.AuthenticationConfig',
    'akira_apps.academic_registration.apps.AcademicRegistrationConfig',
    'akira_apps.academic.apps.AcademicConfig',
    'akira_apps.accounts.apps.AccountsConfig',
    'akira_apps.course.apps.CourseConfig',
    'akira_apps.specialization.apps.SpecializationConfig',
    'akira_apps.shigen.apps.ShigenConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'akira_apps.authentication.middleware.filter_ip_middleware.FilterIPMiddleware',
    'akira_apps.authentication.middleware.userPageTracking_middleware.userPageTrackingMiddleware',
    'akira_apps.authentication.middleware.checkSwitchDeviceRequests_middleware.checkSwitchDeviceRequestsMiddleware',
]

ROOT_URLCONF = 'akira.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'akira.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

#SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '4projtest@gmail.com'
EMAIL_HOST_PASSWORD = 'qwypiocbcstwltgk'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from django.contrib.messages import constants as messages
from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = message_constants.DEBUG

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

SESSION_EXPIRE_AT_BROWSER_CLOSE= True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 14400
SESSION_IDLE_TIMEOUT = 14400
PASSWORD_RESET_TIMEOUT_DAYS = 0.00694444

GOOGLE_RECAPTCHA_SECRET_KEY = '6LfmDxMdAAAAAI9NEfnM3BUqHfF-zAMLLJOwSRw8'
GOOGLE_RECAPTCHA_PUBLIC_KEY = '6LfmDxMdAAAAACs6hML3Ev6wOrB18ZkXSPjNWEvL'