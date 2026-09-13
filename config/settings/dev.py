"""تنظیمات محیط توسعه."""

from .base import *  # noqa: F403
from .base import env, env_list

DEBUG = True

SECRET_KEY = env("SECRET_KEY", "django-insecure-development-key-do-not-use-in-production")

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", ["*"])

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# در توسعه فایل‌های استاتیک بدون manifest سرو شوند تا نیازی به collectstatic نباشد.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

try:
    from .local import *  # noqa: F401,F403
except ImportError:
    pass
