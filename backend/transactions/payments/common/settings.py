"""
Django settings for payments project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from dotenv import load_dotenv

load_dotenv()

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY_PAYMENTS")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["https://jackdrop.online"]

# Application definition

INSTALLED_APPS = [
    'transactions',
    'wallet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'common.urls'

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

WSGI_APPLICATION = 'payments.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
    }
}

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

STATIC_URL = '/transactions/payments/static/'
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PAYMENT_SERVICE_URLS = {
    "create": "https://nicepay.io/public/api/payment",
    "payout": "https://nicepay.io/public/api/payout",
}

PRODUCTS_MICROSERVICE_ROUTES = {
    "deposit-callback": "http://productsapp:8000/products/private/webhook/deposit/",
    "get-free-deposit-case": "http://productsapp:8000/"
                             "products/bonus-buy/deposit-free-case"
                             "/?deposit={deposit}"
}

USERS_MICROSERVICE_ROUTES = {
    "add-depo": "http://usersapp:8000/auth/balances/api/v1/p/add_deposit/",
    "get-info": "http://usersapp:8000/auth/api/v1/p/get_user_info_jwt/"
}

WALLET_ADDRESS = "TBuJ5sCGDzqNgYvzZC67zoTK3eTsDYfKq8"
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

SUCCESS_URL_WITHOUT_FREE_CASE = (
    "https://jackdrop.online/account/"
    "?deposit=1&amount={a}&succes=1"
)
SUCCESS_URL = ("https://jackdrop.online/account/"
               "?deposit=1&amount={a}&succes=1"
               "&free_case={has_free_case}&free_case_img={free_case_img}"
               "&free_case_title={free_case_title}")
FAILED_URL = "https://jackdrop.online/account/"
WEBHOOK_URL = "https://jackdrop.online/transactions/payments/callback/"

PAYMENT_SERVICE_AUTH_HEADER = os.environ.get("AUTH_HEADER")
