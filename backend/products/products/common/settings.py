"""
Django settings for common project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

import dotenv
import sys

dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'cases',
    'items',
    'market',
    'refresher',
    'games',
    'inventory',
    'interactive',
    'bonus',

    'daphne',
    'rest_framework',
    'admin_interface',
    'colorfield',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CSRF_TRUSTED_ORIGINS = ['https://jackdrop.online/',
                        'http://localhost:80/',
                        'http://127.0.0.1:800/',
                        "http://95.163.231.175/"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'common.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
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

ASGI_APPLICATION = 'common.asgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if "test" in sys.argv:
    DATABASES["default"] = DATABASES["test"]

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

STATIC_URL = '/products/static/'

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'uploads/'

MEDIA_ROOT = BASE_DIR

LOCALE_PATHS = [
    BASE_DIR / 'locale'
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = f"redis://productsredis:6379/0"

CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_TIMEZONE = 'Europe/London'

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

GAMES_SERVICE_ROUTES = {
    "drop": "http://gamesapp:8000/games/private/case/drop/",
    "upgrade": "http://gamesapp:8000/games/private/upgrade/new/",
    "contract_get_amount":
        "http://gamesapp:8000/games/private/contract/get_shifted_amount/",
    "contract_save": "http://gamesapp:8000/games/private/contract/save/",
    "create_battle_request":
        "http://gamesapp:8000/games/private/battle/make-request/",
    "drop_battle_request": "http://gamesapp:8000/games/private/battle/drop-request"
                           "/{initiator_id}/",
    "get_battle_requests":  "http://gamesapp:8000/games/private/battle/drop-request"
                           "/all/{case_id}/",
    "get_battle_requests_count": "http://gamesapp:8000/games/private/battle/drop-request"
                           "/all/",
    "make_battle": "http://gamesapp:8000/games/private/battle/make-battle/",
    "make_mines_game": "http://gamesapp:8000/games/private/mines/make/",
    "next_mines_game": "http://gamesapp:8000/games/private/mines/next/",
    "stop_mines_game": "http://gamesapp:8000/games/private/mines/stop/",
    "get_prize_type_wheel": "http://gamesapp:8000/games/private/fortune/prize-type/",
    "get_prize_wheel": "http://gamesapp:8000/games/private/fortune/make-prize/",
    "get_battle_stats": "http://gamesapp:8000/games/private/battle/stats/{user_id}/",
    "get_battles": "http://gamesapp:8000/games/private/battle/all/{user_id}/",
    "get_timeout_wheel": "http://gamesapp:8000/games/private/fortune/get"
                         "-timeout/{user_id}/",
    "use_fortune_promo": "http://gamesapp:8000/games/private/fortune/use-promo/"
}

USERS_MICROSERVICE_ROUTES = {
    "get_advantage": "http://usersapp:8000/auth/api/v1/p/advantage/",
    "get_info": "http://usersapp:8000/auth/api/v1/p/get_user_info_jwt/",
    "bulk_get_info": "http://usersapp:8000/auth/api/v1/p/get_users_info/",
    "get_balance": "http://usersapp:8000/auth/"
                   "balances/api/v1/p/displayed_balance_jwt/",
    "update_balance_jwt": "http://usersapp:8000/auth/"
                          "balances/api/v1/p/displayed_balance_jwt/update/",
    "update_balance": "http://usersapp:8000/auth/"
                      "balances/api/v1/p/displayed_balance/{client_id}/update/",
    "update_hidden_balance": "http://usersapp:8000/auth/"
                             "balances/api/v1/p/hidden_balance/{client_id}/update/",
    "update_advantage": "http://usersapp:8000/auth/api/v1/p/advantage/update/",
    "update_advantage_by_id": "http://usersapp:8000/auth/api/v1/p/advantage/update/{user_id}/",
    "add_user_lose": "http://usersapp:8000/auth/referrals/api/v1/p/add-lose/",
}

CORE_MICROSERVICE_ROUTES = {
    "get_funds": "http://coreapp:8000/private/api/v1/funds/get"
                 "-displayed/",
    "increase_site_funds": "http://coreapp:8000/private/api/v1/funds"
                           "/increase/",
    "decrease_site_funds": "http://coreapp:8000/private/api/v1/funds"
                           "/decrease/",
}

TRANSACTIONS_MICROSERVICE_ROUTES = {
    "add_schedule_item": "http://tmarketapp:8000/transactions/market/schedule/add/",
    "validate_deposit": "http://usersapp:8000/transactions/payments/validate/"
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}
