import os
from .base import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


print("🔥 USING LOCAL SETTINGS 🔥")

# -------------------------
# Core
# -------------------------
DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

ALLOWED_HOSTS = ["*"]

# -------------------------
# Database
# -------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -------------------------
# Wagtail
# -------------------------
WAGTAILADMIN_BASE_URL = "http://127.0.0.1:8000"

# -------------------------
# Supabase Storage (S3)
# -------------------------
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# -------------------------
# Django 4+ storage config
# -------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# # -------------------------
# # Wagtail Markdown Extension
# # -------------------------
# WAGTAILMARKDOWN = {
#     "extensions": ["codehilite"],
#     "extension_configs": {
#         "codehilite": {
#             "css_class": "highlight",
#             "linenums": False,  # Set to True for line numbers
#         }
#     },
# }
