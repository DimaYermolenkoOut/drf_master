"""
Django settings for drfmaster project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import datetime
from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', '0.0.0.0', 'drfmaster.herokuapp.com']

AUTH_USER_MODEL = 'authentication.User'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'django_filters',

    'authentication',
    'expenses',
    'income',
    'drfcalendar',

    'allauth',
    'allauth.account',
    # Optional -- requires install using `django-allauth[socialacocunt]`.
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.telegram',

    "django_celery_beat",
    'django_celery_results',
    "graphene_django",

]
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

ROOT_URLCONF = 'drfmaster.urls'

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
                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'drfmaster.wsgi.application'
GRAPHENE = {
    "SCHEMA": "drfmaster.schema.schema"
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# цей код працює
DATABASES = {
    'default': dj_database_url.config(
        default=f"postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{os.getenv('POSTGRES_DB')}")
}
# цей код краще для doker
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         # 'DB_HOST': os.getenv('DB_HOST'),
#         # для doker
#         'HOST': 'db',
#         'PORT': '5432',
#     }
# }

# for mysql
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'drfmaster',
#         'USER': 'drfmasteruser',
#         'PASSWORD': 'drfmasterpassword',
#         'HOST': 'db',
#         'PORT': '3306',
#     }
# }
# Настройки для SILENCED_SYSTEM_CHECKS
SILENCED_SYSTEM_CHECKS = ["models.W036"]
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
}

AUTHENTICATION_BACKENDS = (

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',

    'django.contrib.auth.backends.ModelBackend',
)

# Provider specific settings
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         'drfmaster': {
#             'client_id': '786254398226-dd0kggua21ref459e0k1bgn7gjbna9ki.apps.googleusercontent.com',
#             'secret': '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',
#             'key': ''
#         }
#     }
# }
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#             # 'https://www.googleapis.com/auth/spreadsheets',
#             # 'https://www.googleapis.com/auth/drive',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'offline',
#         }
#     },
# }
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            # 'https://www.googleapis.com/auth/spreadsheets',
            # 'https://www.googleapis.com/auth/drive',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        }
    },
    'telegram': {
        'dimay_my_bot': {
            'client_id': '7193066110',
            'secret': 'AAF-zjvAp1eDyMTaCphKTYQBhZTePJySZUU',
        },
        'AUTH_PARAMS': {
            'auth_date_validity': 30
        },
    }
}

# Django-allauth
SITE_ID = 2

LOGIN_REDIRECT_URL = '/admin'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_STORE_TOKENS = True


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# google auth https://www.bing.com/chat?form=NTPCHB
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '910422405394-5v18827do2d2321vu6n1ku7f14gpmk0i.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'


# Celery settings
CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
#
# CELERY_BEAT_SCHEDULE = {
#     'hello_world': {
#         'task': 'drfcalendar.tasks.hello_world',
#         'schedule': 2.0,
#     },
#     'another_task': {
#         'task': 'drfcalendar.tasks.process_slots',
#         'schedule': 10.0,
#
#     },
# }

# CELERY_RESULT_BACKEND = "django-db"

