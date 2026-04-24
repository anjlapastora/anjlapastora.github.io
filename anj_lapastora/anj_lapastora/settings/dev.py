from .base import *
import os
from django.core.management.utils import get_random_secret_key

DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

try:
    from .local import *
except ImportError:
    pass
