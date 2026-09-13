"""ابزار ساخت داده‌ی نمونه برای تست‌ها."""

from django.utils import timezone

from blog.models import ArticlePage, Author, BlogIndexPage, Category


def get_index():
    return BlogIndexPage.objects.get()


def create_category(name="پایتون", slug="python", **kwargs):
    return Category.objects.create(name=name, slug=slug, **kwargs)


def create_author(name="سارا محمدی", slug="sara", **kwargs):
    return Author.objects.create(name=name, slug=slug, **kwargs)


def create_article(
    title="اولین مقاله",
    slug="first-article",
    author=None,
    categories=(),
    body=None,
    live=True,
    publish_date=None,
    **kwargs,
):
    index = get_index()
    article = ArticlePage(
        title=title,
        slug=slug,
        intro="چکیده‌ی مقاله",
        author=author,
        live=live,
        publish_date=publish_date or timezone.now(),
        body=body if body is not None else [("paragraph", "<p>متن آزمایشی مقاله.</p>")],
        **kwargs,
    )
    index.add_child(instance=article)
    revision = article.save_revision()
    if live:
        revision.publish()
    article.refresh_from_db()
    if categories:
        article.categories.set(categories)
        article.save()
    return article
