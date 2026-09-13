"""
مدل‌های بلاگ.

سه موجودیت اصلی مطابق نیاز پروژه:
  • ArticlePage  — مقاله (صفحه‌ی Wagtail، دارای پیش‌نویس/انتشار و تاریخچه)
  • Category     — دسته‌بندی (Snippet)
  • Author       — نویسنده (Snippet)

BlogIndexPage ریشه‌ی سایت است و آرشیوها را هم سرو می‌کند.
"""

from django import forms
from django.contrib import admin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.http import Http404
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import Page
from wagtail.search import index

from blog.blocks import ArticleBodyBlock

# میانگین سرعت مطالعه برای محاسبه‌ی «زمان مطالعه» (کلمه در دقیقه).
WORDS_PER_MINUTE = 180


# ---------------------------------------------------------------------------
# تصاویر
# ---------------------------------------------------------------------------
class CustomImage(AbstractImage):
    """مدل تصویر اختصاصی.

    فعلاً فیلد اضافه‌ای ندارد، اما چون مدل تصویر Wagtail بعد از شروع پروژه
    قابل تعویض نیست، از ابتدا اختصاصی تعریف شده تا بعداً بشود فیلد اضافه کرد.
    """

    admin_form_fields = Image.admin_form_fields


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


# ---------------------------------------------------------------------------
# دسته‌بندی
# ---------------------------------------------------------------------------
class Category(index.Indexed, models.Model):
    name = models.CharField("نام", max_length=100, unique=True)
    slug = models.SlugField(
        "اسلاگ",
        max_length=120,
        unique=True,
        allow_unicode=True,
        help_text="در نشانی صفحه استفاده می‌شود: /category/<اسلاگ>/",
    )
    description = models.TextField(
        "توضیح", blank=True, max_length=500, help_text="در صفحه‌ی دسته‌بندی نمایش داده می‌شود."
    )
    image = models.ForeignKey(
        "blog.CustomImage",
        verbose_name="تصویر",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("image"),
    ]

    search_fields = [
        index.SearchField("name"),
        index.AutocompleteField("name"),
        index.SearchField("description"),
    ]

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """نشانی صفحه‌ی آرشیو؛ از مسیرهای BlogIndexPage ساخته می‌شود."""
        index_page = BlogIndexPage.objects.live().first()
        if index_page is None:
            return None
        return index_page.url + index_page.reverse_subpage(
            "category_detail", kwargs={"slug": self.slug}
        )

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def live_articles(self):
        return ArticlePage.objects.live().public().filter(categories=self)

    @admin.display(description="تعداد مقالات")
    def article_count(self):
        return self.live_articles.count()


# ---------------------------------------------------------------------------
# نویسنده
# ---------------------------------------------------------------------------
class Author(index.Indexed, models.Model):
    name = models.CharField("نام و نام خانوادگی", max_length=150)
    slug = models.SlugField(
        "اسلاگ",
        max_length=170,
        unique=True,
        allow_unicode=True,
        help_text="در نشانی صفحه استفاده می‌شود: /author/<اسلاگ>/",
    )
    job_title = models.CharField("عنوان شغلی", max_length=150, blank=True)
    bio = models.TextField("معرفی کوتاه", blank=True, max_length=1000)
    photo = models.ForeignKey(
        "blog.CustomImage",
        verbose_name="تصویر",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    email = models.EmailField("ایمیل", blank=True)
    website = models.URLField("وب‌سایت", blank=True)
    linkedin = models.URLField("لینکدین", blank=True)
    x_profile = models.URLField("ایکس (توییتر)", blank=True)
    telegram = models.URLField("تلگرام", blank=True)
    instagram = models.URLField("اینستاگرام", blank=True)
    user = models.OneToOneField(
        "auth.User",
        verbose_name="کاربر پنل",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="author_profile",
        help_text="اختیاری: اتصال این نویسنده به یک کاربر پنل مدیریت.",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("slug"),
                FieldPanel("job_title"),
                FieldPanel("photo"),
                FieldPanel("bio"),
            ],
            heading="مشخصات",
        ),
        MultiFieldPanel(
            [
                FieldPanel("email"),
                FieldPanel("website"),
                FieldPanel("linkedin"),
                FieldPanel("x_profile"),
                FieldPanel("telegram"),
                FieldPanel("instagram"),
            ],
            heading="راه‌های ارتباطی",
        ),
        FieldPanel("user"),
    ]

    search_fields = [
        index.SearchField("name"),
        index.AutocompleteField("name"),
        index.SearchField("job_title"),
        index.SearchField("bio"),
    ]

    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسندگان"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """نشانی صفحه‌ی آرشیو؛ از مسیرهای BlogIndexPage ساخته می‌شود."""
        index_page = BlogIndexPage.objects.live().first()
        if index_page is None:
            return None
        return index_page.url + index_page.reverse_subpage(
            "author_detail", kwargs={"slug": self.slug}
        )

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def social_links(self):
        fields = [
            ("وب‌سایت", self.website),
            ("لینکدین", self.linkedin),
            ("ایکس", self.x_profile),
            ("تلگرام", self.telegram),
            ("اینستاگرام", self.instagram),
        ]
        return [(label, url) for label, url in fields if url]

    @property
    def live_articles(self):
        return ArticlePage.objects.live().public().filter(author=self)

    @admin.display(description="تعداد مقالات")
    def article_count(self):
        return self.live_articles.count()


# ---------------------------------------------------------------------------
# مقاله
# ---------------------------------------------------------------------------
class ArticlePage(Page):
    cover_image = models.ForeignKey(
        "blog.CustomImage",
        verbose_name="تصویر شاخص",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro = models.TextField(
        "چکیده",
        max_length=300,
        blank=True,
        help_text="در فهرست مقالات و توضیحات متای صفحه استفاده می‌شود.",
    )
    body = StreamField(ArticleBodyBlock(), verbose_name="بدنه", blank=True)
    author = models.ForeignKey(
        "blog.Author",
        verbose_name="نویسنده",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles",
    )
    categories = ParentalManyToManyField(
        "blog.Category", verbose_name="دسته‌بندی‌ها", blank=True, related_name="articles"
    )
    publish_date = models.DateTimeField(
        "تاریخ انتشار",
        default=timezone.now,
        db_index=True,
        help_text="ترتیب نمایش مقالات بر اساس این تاریخ است.",
    )
    featured = models.BooleanField(
        "مقاله‌ی ویژه", default=False, help_text="در بالای فهرست مقالات برجسته می‌شود."
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("author"),
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
                FieldPanel("publish_date"),
                FieldPanel("featured"),
            ],
            heading="اطلاعات مقاله",
        ),
        FieldPanel("intro"),
        FieldPanel("cover_image"),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
        index.AutocompleteField("title"),
        index.FilterField("publish_date"),
        index.RelatedFields("author", [index.SearchField("name")]),
        index.RelatedFields("categories", [index.SearchField("name")]),
    ]

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    @cached_property
    def plain_text(self):
        """متن خام بدنه؛ برای شمارش کلمات و ساخت خلاصه."""
        parts = []
        for block in self.body:
            value = block.value
            if hasattr(value, "source"):  # RichText
                parts.append(strip_tags(value.source))
            elif isinstance(value, str):
                parts.append(strip_tags(value))
            elif hasattr(value, "get"):  # StructValue
                for key in ("text", "code", "title", "caption"):
                    sub = value.get(key)
                    if sub:
                        parts.append(strip_tags(getattr(sub, "source", str(sub))))
        return " ".join(parts)

    @property
    def reading_time(self):
        """زمان تقریبی مطالعه به دقیقه."""
        words = len(self.plain_text.split())
        return max(1, round(words / WORDS_PER_MINUTE))

    @property
    def summary(self):
        if self.intro:
            return self.intro
        text = self.plain_text
        return text[:200] + "…" if len(text) > 200 else text

    @property
    def social_image(self):
        if self.cover_image:
            return self.cover_image
        settings_obj = BlogSettings.for_site(self.get_site())
        return settings_obj.default_social_image

    @property
    def related_articles(self):
        """تا ۳ مقاله‌ی مرتبط بر اساس دسته‌بندی مشترک."""
        queryset = (
            ArticlePage.objects.live()
            .public()
            .exclude(pk=self.pk)
            .filter(categories__in=self.categories.all())
            .distinct()
            .order_by("-publish_date")
        )
        return queryset.select_related("author", "cover_image")[:3]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["related_articles"] = self.related_articles
        return context


# ---------------------------------------------------------------------------
# صفحه‌ی فهرست (ریشه‌ی سایت)
# ---------------------------------------------------------------------------
class BlogIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(
        "توضیح", blank=True, features=["bold", "italic", "link"]
    )
    articles_per_page = models.PositiveSmallIntegerField("تعداد مقاله در هر صفحه", default=12)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("articles_per_page"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["blog.ArticlePage"]
    max_count = 1

    class Meta:
        verbose_name = "فهرست مقالات"
        verbose_name_plural = "فهرست مقالات"

    # --- کمکی‌ها ---------------------------------------------------------
    def get_articles(self):
        return (
            ArticlePage.objects.live()
            .public()
            .descendant_of(self)
            .order_by("-featured", "-publish_date")
            .select_related("author", "cover_image")
            .prefetch_related("categories")
        )

    def paginate(self, request, queryset):
        paginator = Paginator(queryset, self.articles_per_page)
        try:
            return paginator.page(request.GET.get("page", 1))
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)

    # --- مسیرها ----------------------------------------------------------
    @path("")
    def article_list(self, request):
        articles = self.get_articles()
        query = request.GET.get("q", "").strip()
        if query:
            articles = articles.search(query)
        return self.render(
            request,
            context_overrides={
                "articles": self.paginate(request, articles),
                "search_query": query,
            },
        )

    @path("category/")
    def category_list(self, request):
        return self.render(
            request,
            context_overrides={"categories": Category.objects.all()},
            template="blog/category_list.html",
        )

    @path("category/<str:slug>/")
    def category_detail(self, request, slug):
        category = Category.objects.filter(slug=slug).first()
        if category is None:
            raise Http404("دسته‌بندی پیدا نشد.")
        articles = self.get_articles().filter(categories=category)
        return self.render(
            request,
            context_overrides={
                "category": category,
                "articles": self.paginate(request, articles),
            },
            template="blog/category_detail.html",
        )

    @path("author/")
    def author_list(self, request):
        return self.render(
            request,
            context_overrides={"authors": Author.objects.all()},
            template="blog/author_list.html",
        )

    @path("author/<str:slug>/")
    def author_detail(self, request, slug):
        author = Author.objects.filter(slug=slug).first()
        if author is None:
            raise Http404("نویسنده پیدا نشد.")
        articles = self.get_articles().filter(author=author)
        return self.render(
            request,
            context_overrides={
                "author": author,
                "articles": self.paginate(request, articles),
            },
            template="blog/author_detail.html",
        )


# ---------------------------------------------------------------------------
# تنظیمات سایت
# ---------------------------------------------------------------------------
@register_setting(icon="cog")
class BlogSettings(BaseSiteSetting):
    """تنظیمات برندینگ که هر پروژه از پنل تغییرشان می‌دهد."""

    site_title = models.CharField("نام بلاگ", max_length=120, blank=True)
    tagline = models.CharField("شعار / زیرعنوان", max_length=200, blank=True)
    meta_description = models.TextField(
        "توضیح متای پیش‌فرض", blank=True, max_length=300
    )
    logo = models.ForeignKey(
        "blog.CustomImage",
        verbose_name="لوگو",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    favicon = models.ForeignKey(
        "blog.CustomImage",
        verbose_name="فاوآیکون",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    default_social_image = models.ForeignKey(
        "blog.CustomImage",
        verbose_name="تصویر پیش‌فرض اشتراک‌گذاری",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    footer_text = models.CharField("متن پاورقی", max_length=255, blank=True)
    main_site_url = models.URLField(
        "نشانی سایت اصلی",
        blank=True,
        help_text="لینک بازگشت از بلاگ به سایت اصلی پروژه.",
    )
    linkedin = models.URLField("لینکدین", blank=True)
    x_profile = models.URLField("ایکس (توییتر)", blank=True)
    telegram = models.URLField("تلگرام", blank=True)
    instagram = models.URLField("اینستاگرام", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("site_title"),
                FieldPanel("tagline"),
                FieldPanel("meta_description"),
                FieldPanel("main_site_url"),
                FieldPanel("footer_text"),
            ],
            heading="عمومی",
        ),
        MultiFieldPanel(
            [
                FieldPanel("logo"),
                FieldPanel("favicon"),
                FieldPanel("default_social_image"),
            ],
            heading="تصاویر برند",
        ),
        MultiFieldPanel(
            [
                FieldPanel("linkedin"),
                FieldPanel("x_profile"),
                FieldPanel("telegram"),
                FieldPanel("instagram"),
            ],
            heading="شبکه‌های اجتماعی",
        ),
    ]

    class Meta:
        verbose_name = "تنظیمات بلاگ"

    @property
    def social_links(self):
        fields = [
            ("لینکدین", self.linkedin),
            ("ایکس", self.x_profile),
            ("تلگرام", self.telegram),
            ("اینستاگرام", self.instagram),
        ]
        return [(label, url) for label, url in fields if url]
