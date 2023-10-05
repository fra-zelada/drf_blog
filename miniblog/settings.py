"""
Django settings for miniblog project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

import cloudinary
import cloudinary.uploader
import cloudinary.api

# Carga las variables de entorno desde .env
import dotenv
dotenv.load_dotenv()

# Configura Cloudinary usando las variables de entorno
cloudinary.config(cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
                  api_key=os.getenv("CLOUDINARY_API_KEY"),
                  api_secret=os.getenv("CLOUDINARY_API_SECRET"))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ezhoq55vdpvg$-c+=1t_9$-%d6xml%#x(#$6cwhhqajv&*1vnp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'miniblog.post',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'sslserver'


]

SSL_CERTIFICATE = '/ssl/cert.pem'
SSL_KEY = '/ssl/key.pem'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",

]

ROOT_URLCONF = 'miniblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'miniblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',

    ),
}


CORS_ALLOWED_ORIGINS = [

    "https://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]

CSRF_TRUSTED_ORIGINS = [

    "https://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]

CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_ALL_ORIGINS = True  # Permitir todas las solicitudes de origen (esto es para desarrollo, en producción, debes configurar esto de manera más restrictiva).


SIMPLE_JWT = {
    # Utiliza tu subclase personalizada en lugar del serializador predeterminado
    "TOKEN_OBTAIN_SERIALIZER": "miniblog.post.serializers.MyTokenObtainPairSerializer",
    # ... Otras configuraciones de SimpleJWT
    'ACCESS_TOKEN_COOKIE_NAME': 'access_token',
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=15),

}

# SECURE_SSL_CERTIFICATE = 'miniblog/ssl/cert.pem'
# SECURE_SSL_KEY = 'miniblog/ssl/key.pem'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
