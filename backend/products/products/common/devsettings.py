from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': 'localhost'
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if "test" in sys.argv:
    DATABASES["default"] = DATABASES["test"]

del STATIC_ROOT

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_URL = '/products/static/'

CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_RESULT_BACKEND = CELERY_BROKER_URL
