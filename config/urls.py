from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps import Sitemap
from wagtail.images import urls as wagtailimages_urls

from blog.feeds import LatestArticlesFeed

admin_path = settings.WAGTAIL_ADMIN_URL.strip("/")

urlpatterns = [
    path(f"{admin_path}/", include(wagtailadmin_urls)),
    path("images/", include(wagtailimages_urls)),
    path("feed/", LatestArticlesFeed(), name="articles_feed"),
    path("sitemap.xml", sitemap, {"sitemaps": {"pages": Sitemap}}, name="sitemap"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
]

if settings.BLOG_API_ENABLED:
    from config.api import api_router

    urlpatterns += [path("api/v2/", api_router.urls)]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# باید آخر از همه باشد: صفحات Wagtail بقیه‌ی مسیرها را می‌گیرند.
urlpatterns += [path("", include(wagtail_urls))]
