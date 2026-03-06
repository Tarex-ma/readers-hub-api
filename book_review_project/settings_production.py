from decouple import config
import dj_database_url

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# =============================================================================
# DATABASE - Use Render's DATABASE_URL
# =============================================================================
import dj_database_url

# Use the DATABASE_URL environment variable that Render automatically provides
# This is set by your blueprint from the 'readers-hub-db' database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=None),
        conn_max_age=600,
        ssl_require=True  # Render requires SSL
    )
}

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CORS
CORS_ALLOWED_ORIGINS = [
    config('FRONTEND_URL', default='http://localhost:3000'),
]

# Email (SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = config('EMAIL_HOST', default=None)
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@readershug.com')
# If email host is not configured (e.g., on Render without env vars), use console backend
if not EMAIL_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# File Storage (AWS S3 for production)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'