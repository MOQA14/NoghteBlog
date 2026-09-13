"""خوراک RSS مقالات."""

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from blog.models import ArticlePage, BlogIndexPage, BlogSettings


class LatestArticlesFeed(Feed):
    feed_type = Rss201rev2Feed
    description_template = None

    def get_object(self, request, *args, **kwargs):
        self.request = request
        return BlogIndexPage.objects.live().first()

    def title(self, obj):
        settings_obj = BlogSettings.for_request(self.request)
        return settings_obj.site_title or (obj.title if obj else "بلاگ")

    def description(self, obj):
        settings_obj = BlogSettings.for_request(self.request)
        return settings_obj.tagline or settings_obj.meta_description or ""

    def link(self, obj):
        return obj.url if obj else "/"

    def items(self, obj):
        if obj is None:
            return ArticlePage.objects.none()
        return (
            ArticlePage.objects.live()
            .public()
            .descendant_of(obj)
            .order_by("-publish_date")
            .select_related("author")[:20]
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return item.url

    def item_pubdate(self, item):
        return item.publish_date

    def item_author_name(self, item):
        return item.author.name if item.author else None
