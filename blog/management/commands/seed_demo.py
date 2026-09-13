"""ساخت محتوای نمونه برای توسعه و کار تیم فرانت.

    python manage.py seed_demo

دستور idempotent است؛ اجرای دوباره داده‌ی تکراری نمی‌سازد.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import ArticlePage, Author, BlogIndexPage, Category

CATEGORIES = [
    ("جنگو", "django", "مقالات مربوط به فریم‌ورک جنگو."),
    ("ویجتیل", "wagtail", "سیستم مدیریت محتوای ویجتیل."),
    ("دواپس", "devops", "استقرار، داکر و زیرساخت."),
]

AUTHORS = [
    ("سارا محمدی", "sara-mohammadi", "توسعه‌دهنده‌ی بک‌اند"),
    ("امیر رضایی", "amir-rezaei", "مهندس دواپس"),
]

ARTICLES = [
    (
        "شروع کار با ویجتیل",
        "getting-started-with-wagtail",
        "ویجتیل یک سیستم مدیریت محتوای مبتنی بر جنگو است که ساختار صفحات را به توسعه‌دهنده می‌سپارد.",
        "wagtail",
        "sara-mohammadi",
        True,
    ),
    (
        "مدل‌سازی محتوا با StreamField",
        "content-modeling-with-streamfield",
        "با StreamField می‌توانید بدنه‌ی مقاله را از بلوک‌های مستقل بسازید.",
        "wagtail",
        "sara-mohammadi",
        False,
    ),
    (
        "بهینه‌سازی کوئری‌ها در جنگو",
        "optimizing-django-queries",
        "با select_related و prefetch_related می‌شود تعداد کوئری‌ها را چشمگیر کم کرد.",
        "django",
        "sara-mohammadi",
        False,
    ),
    (
        "استقرار جنگو با داکر",
        "deploying-django-with-docker",
        "یک ایمیج کوچک و قابل تکرار برای استقرار پروژه‌های جنگو.",
        "devops",
        "amir-rezaei",
        False,
    ),
]


def demo_body(intro):
    return [
        (
            "paragraph",
            "<p>این مقاله‌ی نمونه است و فقط برای دیدن ظاهر صفحه ساخته شده. "
            "چکیده‌ی آن بالای صفحه نمایش داده می‌شود و بدنه از همین‌جا شروع می‌شود.</p>",
        ),
        ("heading", {"text": "چرا این موضوع مهم است؟", "level": "h2"}),
        (
            "paragraph",
            "<p>این یک متن نمونه است تا تیم فرانت بتواند چیدمان و تایپوگرافی "
            "بدنه‌ی مقاله را ببیند. می‌توانید آزادانه تغییرش بدهید.</p>",
        ),
        (
            "callout",
            {
                "style": "tip",
                "title": "پیشنهاد",
                "text": "<p>برای تغییر رنگ‌ها فقط فایل <b>theme.css</b> را ویرایش کنید.</p>",
            },
        ),
        ("quote", {"text": "سادگی، پیش‌نیاز قابلیت اطمینان است.", "attribution": "ادسخر دیکسترا"}),
        ("heading", {"text": "یک نمونه کد", "level": "h2"}),
        (
            "code",
            {
                "language": "python",
                "code": 'articles = ArticlePage.objects.live().order_by("-publish_date")',
            },
        ),
        (
            "paragraph",
            f"<p>{intro} و در پایان، یک پاراگراف دیگر تا زمان مطالعه واقعی‌تر محاسبه شود.</p>",
        ),
    ]


class Command(BaseCommand):
    help = "ساخت دسته‌بندی، نویسنده و مقاله‌ی نمونه"

    def handle(self, *args, **options):
        index = BlogIndexPage.objects.first()
        if index is None:
            self.stderr.write("صفحه‌ی «فهرست مقالات» پیدا نشد. اول migrate را اجرا کنید.")
            return

        categories = {}
        for name, slug, description in CATEGORIES:
            category, created = Category.objects.get_or_create(
                slug=slug, defaults={"name": name, "description": description}
            )
            categories[slug] = category
            if created:
                self.stdout.write(f"دسته‌بندی ساخته شد: {name}")

        authors = {}
        for name, slug, job_title in AUTHORS:
            author, created = Author.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "job_title": job_title,
                    "bio": f"{name}، {job_title}. این معرفی نمونه است.",
                },
            )
            authors[slug] = author
            if created:
                self.stdout.write(f"نویسنده ساخته شد: {name}")

        now = timezone.now()
        for offset, (title, slug, intro, category_slug, author_slug, featured) in enumerate(
            ARTICLES
        ):
            if ArticlePage.objects.filter(slug=slug).exists():
                continue
            article = ArticlePage(
                title=title,
                slug=slug,
                intro=intro,
                body=demo_body(intro),
                author=authors[author_slug],
                featured=featured,
                publish_date=now - timezone.timedelta(days=offset * 3),
            )
            index.add_child(instance=article)
            article.save_revision().publish()
            article.categories.add(categories[category_slug])
            article.save()
            self.stdout.write(f"مقاله ساخته شد: {title}")

        self.stdout.write(self.style.SUCCESS("محتوای نمونه آماده است."))
