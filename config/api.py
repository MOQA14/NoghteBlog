"""
API فقط-خواندنی (Wagtail API v2).

برای وقتی که یک پروژه‌ی دیگر بخواهد مقالات این بلاگ را داخل سایت خودش
نمایش دهد؛ مثلاً «۳ مقاله‌ی آخر» در صفحه‌ی اصلی.

    /api/v2/pages/?type=blog.ArticlePage&fields=title,intro,cover_image&limit=3
    /api/v2/images/

اگر لازمش ندارید، در .env مقدار BLOG_API_ENABLED=false بگذارید.
"""

from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet

api_router = WagtailAPIRouter("wagtailapi")
api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
