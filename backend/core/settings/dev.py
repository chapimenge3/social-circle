from .base import *

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEBUG = True
ALLOWED_HOSTS = ["*"]
AWS_STORAGE_BUCKET_NAME = "social-circle-dev"