"""
Django settings for config project.

مقادیری که بین سرورها فرق می‌کنند از متغیرهای محیطی خوانده می‌شوند
(فایل .env روی هر سرور). کلید اصلی DEBUG است: روی سرورهای dev و prd
مقدار DEBUG=false بگذارید تا تنظیمات امنیتی انتهای فایل فعال شوند.

https://docs.djangoproject.com/en/5.2/topics/settings/
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-me-in-production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes", "on")

# مثال: ALLOWED_HOSTS=blog.example.com,www.blog.example.com
# اگر خالی بماند و DEBUG روشن باشد، جنگو خودش localhost و 127.0.0.1 را
# می‌پذیرد. با DEBUG=false خالی ماندنش یعنی همه‌ی درخواست‌ها رد می‌شوند و
# دستور check --deploy هم هشدار W020 می‌دهد.
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]

# مثال: CSRF_TRUSTED_ORIGINS=https://blog.example.com
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
] or [f"https://{h}" for h in ALLOWED_HOSTS if "*" not in h]


# Application definition

# فقط ماژول‌هایی از Wagtail نصب شده‌اند که برای «مقالات، دسته‌بندی‌ها و
# نویسندگان» لازم‌اند. عمداً نصب نشده‌اند: wagtail.contrib.forms،
# wagtail.contrib.redirects و wagtail.contrib.search_promotions.
# نکته: wagtail.documents نصب است چون پنل مدیریت به آن وابستگی سخت دارد،
# اما در blog/wagtail_hooks.py از منو حذف شده است.
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# بدون DATABASE_URL از SQLite استفاده می‌شود.

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
# با fa بودن زبان، پنل مدیریت Wagtail هم فارسی و راست‌به‌چپ می‌شود.

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "fa")

TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Tehran")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT") or BASE_DIR / "media")
MEDIA_URL = "/media/"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django sets a maximum of 1000 fields per form by default, but particularly complex page models
# can exceed this limit within Wagtail's page editor.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000


# Email

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 25))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "False").lower() in ("true", "1", "yes", "on")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@localhost")


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "[{levelname}] {name}: {message}", "style": "{"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["console"], "level": os.environ.get("LOG_LEVEL", "WARNING")},
}


# Wagtail settings

WAGTAIL_SITE_NAME = os.environ.get("WAGTAIL_SITE_NAME", "بلاگ نقطه")

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "http://localhost:8000")

# مسیر پنل مدیریت؛ برای امنیت بیشتر می‌توانید عوضش کنید (مثلاً panel).
WAGTAIL_ADMIN_URL = os.environ.get("WAGTAIL_ADMIN_URL", "admin")

# گردش‌کار تأیید محتوا لازم نیست؛ همان پیش‌نویس/انتشار ساده کافی است.
WAGTAIL_WORKFLOW_ENABLED = False

# اسلاگ‌های فارسی مجاز باشند (مثل /سلام-دنیا/).
WAGTAIL_ALLOW_UNICODE_SLUGS = True

WAGTAIL_PASSWORD_RESET_ENABLED = False

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {"BACKEND": "wagtail.search.backends.database"},
}

WAGTAILIMAGES_IMAGE_MODEL = "blog.CustomImage"
WAGTAILIMAGES_EXTENSIONS = ["gif", "jpg", "jpeg", "png", "webp", "avif", "svg"]
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

WAGTAILEMBEDS_RESPONSIVE_HTML = True

# امکانات ویرایشگر متن غنی. درج سند (document-link) عمداً نیست.
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

# API فقط-خواندنی برای وقتی که پروژه‌ای بخواهد مقالات را داخل سایت خودش
# نمایش دهد. با BLOG_API_ENABLED=false خاموش می‌شود.
BLOG_API_ENABLED = os.environ.get("BLOG_API_ENABLED", "True").lower() in ("true", "1", "yes", "on")


# Deployment settings
# https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
# روی سرورهای dev و prd مقدار DEBUG=false بگذارید تا این‌ها فعال شوند.

if not DEBUG:
    # نام فایل‌های استاتیک hash می‌گیرد تا کش مرورگر خودکار باطل شود.
    STORAGES["staticfiles"]["BACKEND"] = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )

    # پشت ریورس‌پروکسی (traefik در dokploy) اجرا می‌شود.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True

    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"
else:
    EMAIL_BACKEND = os.environ.get(
        "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
    )
