"""
تنظیمات پایه‌ی NoghteBlog (Wagtail).

این فایل مشترک بین همه‌ی محیط‌هاست. مقادیر محیطی از متغیرهای محیط (.env)
خوانده می‌شوند تا همین یک ایمیج در پروژه‌های مختلف قابل استفاده باشد.
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# در محیط توسعه فایل .env خوانده می‌شود؛ در پروداکشن متغیرها را dokploy تزریق می‌کند.
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

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# صفحه‌ساز Wagtail می‌تواند از سقف پیش‌فرض ۱۰۰۰ فیلد فرم عبور کند.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

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
