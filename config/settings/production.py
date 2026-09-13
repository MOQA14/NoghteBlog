"""تنظیمات محیط پروداکشن (dokploy / docker)."""

from .base import *  # noqa: F403
from .base import env, env_bool, env_list

DEBUG = False

SECRET_KEY = env("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("متغیر محیطی SECRET_KEY برای اجرای پروداکشن الزامی است.")

# مثال: ALLOWED_HOSTS=blog.example.com
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise RuntimeError("متغیر محیطی ALLOWED_HOSTS برای اجرای پروداکشن الزامی است.")

# مثال: CSRF_TRUSTED_ORIGINS=https://blog.example.com
CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS", [f"https://{host}" for host in ALLOWED_HOSTS if "*" not in host]
)

# پشت ریورس‌پروکسی (traefik در dokploy) اجرا می‌شود.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = env_bool("USE_X_FORWARDED_HOST", True)

SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", True)
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", True)
SECURE_HSTS_SECONDS = int(env("SECURE_HSTS_SECONDS", 60 * 60 * 24 * 30))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", False)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# ایمیل (اختیاری؛ برای اعلان‌های پنل)
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", "localhost")
EMAIL_PORT = int(env("EMAIL_PORT", 25))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", False)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "noreply@localhost")
