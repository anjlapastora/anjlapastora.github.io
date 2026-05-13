import os
import dj_database_url
from .base import *

print("🔥 USING PRODUCTION SETTINGS 🔥")

# -------------------------
# Core
# -------------------------
DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# -------------------------
# Database
# -------------------------
DATABASES = {
    "default": dj_database_url.parse(
        os.environ["DATABASE_URL"],
        conn_max_age=60,
        ssl_require=True,
    )
}

# -------------------------
# Security
# -------------------------
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# -------------------------
# Wagtail
# -------------------------
WAGTAILADMIN_BASE_URL = "https://anj-lapastora.onrender.com"

# -------------------------
# Supabase Storage (S3)
# -------------------------
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = "media"

AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = "ap-southeast-1"
AWS_S3_SIGNATURE_VERSION = "s3v4"

AWS_S3_ADDRESSING_STYLE = "path"

AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

# -------------------------
# Django 4+ storage config
# -------------------------
STORAGES = {
    "default": {
        "BACKEND": "anj_lapastora.storage_backends.SupabaseStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# -------------------------
# Higher text/form submission
# -------------------------
DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400

FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400
