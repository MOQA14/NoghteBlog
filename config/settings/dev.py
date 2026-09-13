"""تنظیمات محیط توسعه."""

from .base import *  # noqa: F403
from .base import env

DEBUG = True

SECRET_KEY = env("SECRET_KEY", "django-insecure-development-key-do-not-use-in-production")

# در توسعه عمداً از متغیر محیطی خوانده نمی‌شود: اگر کسی یک .env مربوط به
# پروداکشن را کپی کند، اجرای لوکال نباید با خطای DisallowedHost بشکند.
ALLOWED_HOSTS = ["*"]

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
