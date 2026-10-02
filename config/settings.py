"""
تنظیمات NoghteBlog.

یک فایل برای همه‌ی محیط‌ها. تفاوت dev و prd فقط از راه متغیرهای محیطی
(فایل .env روی هر سرور) تعیین می‌شود، نه از راه ماژول‌های جدا.

کلید اصلی، متغیر DEBUG است:
  DEBUG=true   → حالت توسعه: کلید و دامنه‌ی پیش‌فرض، بدون اجبار HTTPS
  DEBUG=false  → حالت استقرار: SECRET_KEY و ALLOWED_HOSTS الزامی، HTTPS و
                 کوکی امن و HSTS روشن، فایل‌های استاتیک با manifest
هر کدام از این‌ها را می‌شود جداگانه با متغیر محیطی بازنویسی کرد.
"""

import os
import sys
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# در توسعه فایل .env خوانده می‌شود؛ در پروداکشن متغیرها را dokploy تزریق می‌کند.
load_dotenv(BASE_DIR / ".env")


def env(key, default=None):
    value = os.environ.get(key)
    return default if value is None or value == "" else value


def env_bool(key, default=False):
    value = env(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(key, default=()):
    value = env(key)
    if value is None:
        return list(default)
    return [item.strip() for item in value.split(",") if item.strip()]


# ---------------------------------------------------------------------------
# حالت اجرا
# ---------------------------------------------------------------------------
DEBUG = env_bool("DEBUG", False)

# هنگام اجرای تست‌ها نباید نبودِ SECRET_KEY یا ALLOWED_HOSTS جلوی کار را بگیرد
# و فایل‌های استاتیک هم نباید manifest لازم داشته باشند.
TESTING = "test" in sys.argv

# تنها حالتی که سخت‌گیری کامل لازم است: اجرای واقعی با DEBUG=false
STRICT = not DEBUG and not TESTING

# ---------------------------------------------------------------------------
# امنیت پایه
# ---------------------------------------------------------------------------
SECRET_KEY = env("SECRET_KEY")
if not SECRET_KEY:
    if STRICT:
        raise ImproperlyConfigured(
            "متغیر محیطی SECRET_KEY الزامی است. "
            "ساخت کلید: python -c \"from django.core.management.utils import "
            'get_random_secret_key as k; print(k())"'
        )
    SECRET_KEY = "django-insecure-development-key-do-not-use-in-production"

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    if STRICT:
        raise ImproperlyConfigured(
            "متغیر محیطی ALLOWED_HOSTS الزامی است، مثلا blog.example.com . "
            "برای اجرای لوکال: cp .env.example .env"
        )
    ALLOWED_HOSTS = ["*"]

# مثال: CSRF_TRUSTED_ORIGINS=https://blog.example.com
# اگر داده نشود، از روی ALLOWED_HOSTS ساخته می‌شود.
CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    [f"https://{host}" for host in ALLOWED_HOSTS if "*" not in host],
)

# ---------------------------------------------------------------------------
# اپلیکیشن‌ها
# ---------------------------------------------------------------------------
# فقط ماژول‌هایی از Wagtail نصب شده‌اند که برای «مقالات، دسته‌بندی‌ها و
# نویسندگان» لازم‌اند. عمداً نصب نشده‌اند:
#   wagtail.contrib.forms          (فرم‌ساز)
#   wagtail.contrib.redirects      (ریدایرکت‌ها)
#   wagtail.contrib.search_promotions
#
# نکته: wagtail.documents نصب است چون پنل مدیریت Wagtail به آن وابستگی
# سخت دارد، اما در blog/wagtail_hooks.py از منو حذف شده و در ویرایشگر
# متن غنی هم امکان درج سند فعال نیست.
INSTALLED_APPS = [
    "blog",
    "wagtail.api.v2",
    "wagtail.contrib.sitemaps",
    "wagtail.contrib.settings",
    "wagtail.contrib.routable_page",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django_filters",
    "rest_framework",
    "django.contrib.auth",
    "django.contrib.sitemaps",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # BASE_DIR/templates اول می‌آید تا تیم فرانت بتواند هر قالبی را
        # بدون دست زدن به کد پایتون بازنویسی کند.
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# دیتابیس
# ---------------------------------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=int(env("DB_CONN_MAX_AGE", "600")),
        conn_health_checks=True,
    )
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# زبان و زمان
# ---------------------------------------------------------------------------
# با fa بودن زبان، پنل مدیریت Wagtail هم فارسی و راست‌به‌چپ می‌شود.
LANGUAGE_CODE = env("LANGUAGE_CODE", "fa")
TIME_ZONE = env("TIME_ZONE", "Asia/Tehran")
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# فایل‌های استاتیک و رسانه
# ---------------------------------------------------------------------------
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = env("STATIC_URL", "/static/")

MEDIA_ROOT = Path(env("MEDIA_ROOT", BASE_DIR / "media"))
MEDIA_URL = env("MEDIA_URL", "/media/")

# نام فایل‌های استاتیک فقط در استقرار hash می‌گیرد. در توسعه و تست این کار
# لازم نیست و نبودِ فایل manifest باعث خطا می‌شود.
STATICFILES_BACKEND = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
    if STRICT
    else "django.contrib.staticfiles.storage.StaticFilesStorage"
)

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": STATICFILES_BACKEND},
}

# صفحه‌ساز Wagtail می‌تواند از سقف پیش‌فرض ۱۰۰۰ فیلد فرم عبور کند.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

# ---------------------------------------------------------------------------
# امنیت هنگام استقرار
# ---------------------------------------------------------------------------
# پشت ریورس‌پروکسی (traefik در dokploy) اجرا می‌شود.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = env_bool("USE_X_FORWARDED_HOST", STRICT)

SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", STRICT)
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", STRICT)
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", STRICT)
SECURE_HSTS_SECONDS = int(env("SECURE_HSTS_SECONDS", 60 * 60 * 24 * 30 if STRICT else 0))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", STRICT)
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", False)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# ---------------------------------------------------------------------------
# ایمیل
# ---------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"
    if STRICT
    else "django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = env("EMAIL_HOST", "localhost")
EMAIL_PORT = int(env("EMAIL_PORT", 25))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", False)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "noreply@localhost")

# ---------------------------------------------------------------------------
# Wagtail
# ---------------------------------------------------------------------------
WAGTAIL_SITE_NAME = env("WAGTAIL_SITE_NAME", "بلاگ نقطه")
WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL", "http://localhost:8000")
# مسیر پنل مدیریت؛ برای امنیت بیشتر می‌توانید عوضش کنید (مثلاً panel).
WAGTAIL_ADMIN_URL = env("WAGTAIL_ADMIN_URL", "admin")

# گردش‌کار تأیید محتوا لازم نیست؛ همان پیش‌نویس/انتشار ساده کافی است.
WAGTAIL_WORKFLOW_ENABLED = False
# اسلاگ‌های فارسی مجاز باشند (مثل /سلام-دنیا/). برای اسلاگ لاتین: False
WAGTAIL_ALLOW_UNICODE_SLUGS = env_bool("WAGTAIL_ALLOW_UNICODE_SLUGS", True)
WAGTAIL_PASSWORD_RESET_ENABLED = env_bool("WAGTAIL_PASSWORD_RESET_ENABLED", False)
WAGTAILADMIN_COMMENTS_ENABLED = True

WAGTAILSEARCH_BACKENDS = {
    "default": {"BACKEND": "wagtail.search.backends.database"},
}

WAGTAILIMAGES_IMAGE_MODEL = "blog.CustomImage"
WAGTAILIMAGES_EXTENSIONS = ["gif", "jpg", "jpeg", "png", "webp", "avif", "svg"]
WAGTAILIMAGES_MAX_UPLOAD_SIZE = int(env("WAGTAILIMAGES_MAX_UPLOAD_SIZE", 10 * 1024 * 1024))

# سرویس‌های امبد مجاز در بدنه‌ی مقاله (ویدیو و ...).
WAGTAILEMBEDS_RESPONSIVE_HTML = True

# ---------------------------------------------------------------------------
# ویرایشگر متن غنی
# ---------------------------------------------------------------------------
# امکاناتی مثل درج سند (document-link) عمداً حذف شده‌اند.
RICH_TEXT_FEATURES = [
    "h2",
    "h3",
    "h4",
    "bold",
    "italic",
    "link",
    "ol",
    "ul",
    "hr",
    "blockquote",
    "code",
    "superscript",
    "subscript",
    "strikethrough",
]

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {"features": RICH_TEXT_FEATURES},
    },
}

# ---------------------------------------------------------------------------
# API فقط-خواندنی (اختیاری)
# ---------------------------------------------------------------------------
# اگر پروژه‌ای بخواهد مقالات را داخل سایت خودش نمایش دهد (مثلاً «۳ مقاله‌ی
# آخر» در صفحه‌ی اصلی)، این API آماده است. با BLOG_API_ENABLED=false خاموش می‌شود.
BLOG_API_ENABLED = env_bool("BLOG_API_ENABLED", True)

# ---------------------------------------------------------------------------
# لاگ
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "[{levelname}] {name}: {message}", "style": "{"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "root": {"handlers": ["console"], "level": env("LOG_LEVEL", "INFO")},
}

# ---------------------------------------------------------------------------
# تنظیمات مخصوص اجرای تست‌ها
# ---------------------------------------------------------------------------
if TESTING:
    # دیتابیس در حافظه، بدون نوشتن فایل روی دیسک
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
        "staticfiles": {"BACKEND": STATICFILES_BACKEND},
    }
    # WhiteNoise در تست لازم نیست و بدون collectstatic هشدار می‌دهد.
    MIDDLEWARE = [m for m in MIDDLEWARE if "whitenoise" not in m]
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {"null": {"class": "logging.NullHandler"}},
        "root": {"handlers": ["null"], "level": "CRITICAL"},
    }
