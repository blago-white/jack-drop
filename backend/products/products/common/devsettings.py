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
