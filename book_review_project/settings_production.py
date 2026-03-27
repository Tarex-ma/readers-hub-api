import os
from pathlib import Path
from decouple import config
import dj_database_url
from .settings import *

# Cloudinary imports
import cloudinary
import cloudinary.uploader
import cloudinary.api
BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# SECURITY
# ===============================

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS
allowed_hosts_env = config('ALLOWED_HOSTS', default='')

ALLOWED_HOSTS = [
    host.strip()
    for host in allowed_hosts_env.split(',')
    if host.strip()
]

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['readers-hub-api.onrender.com']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = 'DENY'

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# ===============================
# DATABASE (Render PostgreSQL)
# ===============================

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}


# ===============================
# MIDDLEWARE
# ===============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ===============================
# STATIC FILES
# ===============================

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# MEDIA FILES - CLOUDINARY
# ===============================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dvqnpkbbm',     
    'API_KEY': '671673844455157',           
    'API_SECRET': 'vKas0pu1zPSoXavj0V88W7nwDbs',    
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
    secure=True
)
# ===============================
# MEDIA FILES
# ===============================

if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ===============================
# CORS - FIXED: Allow both localhost and Vercel
# ===============================

# Get frontend URL from environment or use default
frontend_url = config('FRONTEND_URL', default='http://localhost:5173')

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",                    # Local development
    "http://127.0.0.1:5173",                    # Local development alternative
    "https://readers-hub-frontend.vercel.app",  # Your production frontend
    "https://readers-hub-frontend-agwp-4431tl0vw-tarikumato-7369s-projects.vercel.app",
]

# If FRONTEND_URL is set in environment and not already in list, add it
if frontend_url not in CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS.append(frontend_url)

CORS_ALLOW_CREDENTIALS = True

# Allow all methods (GET, POST, PUT, DELETE, etc.)
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
]
# Allow these headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# ===============================
# CSRF - FIXED: Add Vercel domain
# ===============================

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://readers-hub-frontend.vercel.app",
    "https://readers-hub-frontend-agwp-4431tl0vw-tarikumato-7369s-projects.vercel.app",
]

if frontend_url not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(frontend_url)


# ===============================
# EMAIL
# ===============================

EMAIL_HOST = config('EMAIL_HOST', default=None)

if EMAIL_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@readershub.com')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ===============================
# REST FRAMEWORK
# ===============================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}


# ===============================
# LOGGING
# ===============================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },

    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
    },
}