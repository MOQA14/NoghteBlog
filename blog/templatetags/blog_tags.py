"""فیلترها و تگ‌های قالب مخصوص بلاگ."""

from django import template
from django.utils import timezone

from blog.models import Author, Category

register = template.Library()

PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

JALALI_MONTHS = [
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
]

try:
    import jdatetime

    JALALI_AVAILABLE = True
except ImportError:  # pragma: no cover - وابستگی اختیاری
    JALALI_AVAILABLE = False


@register.filter
def persian_digits(value):
    """۱۲۳ به جای 123."""
    return str(value).translate(PERSIAN_DIGITS)


@register.filter
def jalali(value, fmt="long"):
    """تبدیل تاریخ میلادی به شمسی. fmt: long | short | numeric

    اگر jdatetime نصب نباشد، تاریخ میلادی برگردانده می‌شود.
    """
    if not value:
        return ""
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    if not JALALI_AVAILABLE:
        return value.strftime("%Y/%m/%d")

    jalali_date = jdatetime.datetime.fromgregorian(datetime=value)
    month_name = JALALI_MONTHS[jalali_date.month - 1]
    if fmt == "numeric":
        text = f"{jalali_date.year}/{jalali_date.month:02d}/{jalali_date.day:02d}"
    elif fmt == "short":
        text = f"{jalali_date.day} {month_name}"
    else:
        text = f"{jalali_date.day} {month_name} {jalali_date.year}"
    return text.translate(PERSIAN_DIGITS)


@register.filter
def iso_date(value):
    """برای ویژگی datetime در تگ <time>."""
    if not value:
        return ""
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    return value.isoformat()


@register.simple_tag
def all_categories():
    return Category.objects.all()


@register.simple_tag
def all_authors():
    return Author.objects.all()


@register.simple_tag(takes_context=True)
def querystring_replace(context, **kwargs):
    """کوئری‌استرینگ فعلی را با مقادیر جدید بازمی‌سازد (برای صفحه‌بندی)."""
    request = context["request"]
    params = request.GET.copy()
    for key, value in kwargs.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = value
    return params.urlencode()
