"""
Django settings for Research project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x0!h!zt6!3=bejl2bbm3!y#vq87)7s%3_@ei^q9!+)2!rczpxm'

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
    'myapp',
    'agriculture',
     'crispy_forms',
     
     'crispy_bootstrap4',  # For Bootstrap 4
# 'django.contrib.gis',
# 'satellite',

    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
 
]

ROOT_URLCONF = 'Research.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
      'DIRS': [BASE_DIR / 'templates'],  # Add your templates directory

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

WSGI_APPLICATION = 'Research.wsgi.application'
CRISPY_TEMPLATE_PACK = 'bootstrap4'   


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'Research',
        'USER':'root',
        'PASSWORD':'',
        'HOST':'localhost',
        'PORT':'3306',
 'OPTIONS': {
            'init_command': "SET default_storage_engine=INNODB;",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
  
STATICFILES_DIRS = [
    BASE_DIR / "static",  
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # 
EMAIL_PORT = 587  # Typically 587 for TLS
EMAIL_USE_TLS = True  # Use TLS for secure connections
EMAIL_HOST_USER = 'mohamedabdinooor701@gmail.com'  # Replace with your email address
EMAIL_HOST_PASSWORD = '@aBDINOOR15514'  # Replace with your email password or app password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SESSION_COOKIE_AGE = 1209600  # Two weeks, adjust as needed
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = '/login/'   
import os
OPENAI_API_KEY = "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",

 # settings.py
GEOCODING_API_KEY = '68135bd75f2f7367908099jtkaa61a6'
OPENWEATHER_API_KEY = '5945d58a93e4205381d49e226f7c22ac'

