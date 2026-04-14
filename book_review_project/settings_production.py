import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ===============================
# SECURITY
# ===============================
SECRET_KEY = config("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# ===============================
# CORE DJANGO SETTINGS
# ===============================
ROOT_URLCONF = "book_review_project.urls"
WSGI_APPLICATION = "book_review_project.wsgi.application"

AUTH_USER_MODEL = "accounts.CustomUser"

# ===============================
# INSTALLED APPS
# ===============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "cloudinary",
    "cloudinary_storage",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "drf_yasg",

    # Your apps
    "accounts",
    "books",
    "activities",
    "comments",
]

# ===============================
# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ===============================
# TEMPLATES (REQUIRED FOR ADMIN)
# ===============================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ===============================
# DATABASE (Neon / PostgreSQL)
# ===============================
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# ===============================
# STATIC FILES (WhiteNoise)
# ===============================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ===============================
# MEDIA FILES (Cloudinary ONLY)
# ===============================
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

# ❌ REMOVE THIS (critical)
# MEDIA_ROOT = ...
# MEDIA_URL = ...

# ===============================
# REST FRAMEWORK
# ===============================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}

# ===============================
# CORS
# ===============================
CORS_ALLOW_ALL_ORIGINS = True

# ===============================
# TIME
# ===============================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ===============================
# SECURITY (Render / HTTPS)
# ===============================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ===============================
# DEFAULT FIELD
# ===============================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"