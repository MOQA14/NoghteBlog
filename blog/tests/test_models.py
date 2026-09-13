from django.test import TestCase
from django.utils import timezone

from blog.models import ArticlePage, BlogIndexPage
from blog.tests.factories import create_article, create_author, create_category, get_index


class BlogIndexTests(TestCase):
    def test_index_page_created_by_migration_and_is_site_root(self):
        index = get_index()
        self.assertEqual(BlogIndexPage.objects.count(), 1)
        self.assertEqual(index.url, "/")

    def test_only_one_index_page_allowed(self):
        self.assertEqual(BlogIndexPage.max_count, 1)

    def test_articles_are_ordered_by_featured_then_date(self):
        now = timezone.now()
        create_article(title="قدیمی", slug="old", publish_date=now - timezone.timedelta(days=2))
        create_article(title="جدید", slug="new", publish_date=now)
        create_article(
            title="ویژه", slug="featured", featured=True,
            publish_date=now - timezone.timedelta(days=5),
        )
        titles = [article.title for article in get_index().get_articles()]
        self.assertEqual(titles, ["ویژه", "جدید", "قدیمی"])

    def test_draft_articles_are_excluded(self):
        create_article(title="پیش‌نویس", slug="draft", live=False)
        self.assertEqual(get_index().get_articles().count(), 0)


class ArticleTests(TestCase):
    def test_reading_time_is_at_least_one_minute(self):
        article = create_article()
        self.assertGreaterEqual(article.reading_time, 1)

    def test_reading_time_grows_with_content(self):
        long_body = [("paragraph", "<p>" + ("کلمه " * 900) + "</p>")]
        article = create_article(slug="long", body=long_body)
        self.assertEqual(article.reading_time, 5)

    def test_plain_text_strips_html(self):
        article = create_article(body=[("paragraph", "<p>سلام <strong>دنیا</strong></p>")])
        self.assertEqual(article.plain_text.strip(), "سلام دنیا")

    def test_summary_falls_back_to_body(self):
        article = create_article(body=[("paragraph", "<p>متن بدنه</p>")])
        article.intro = ""
        self.assertIn("متن بدنه", article.summary)

    def test_article_can_only_live_under_index(self):
        self.assertEqual(ArticlePage.parent_page_types, ["blog.BlogIndexPage"])
        self.assertEqual(ArticlePage.subpage_types, [])

    def test_related_articles_share_a_category(self):
        category = create_category()
        other = create_category(name="جنگو", slug="django")
        first = create_article(slug="a", title="الف", categories=[category])
        create_article(slug="b", title="ب", categories=[category])
        create_article(slug="c", title="ج", categories=[other])
        related = list(first.related_articles)
        self.assertEqual([article.title for article in related], ["ب"])


class CategoryTests(TestCase):
    def test_url_points_to_index_route(self):
        category = create_category()
        self.assertEqual(category.url, "/category/python/")

    def test_unicode_slug_is_allowed(self):
        """اسلاگ فارسی مجاز است؛ در نشانی به شکل percent-encoded درمی‌آید."""
        category = create_category(name="برنامه‌نویسی", slug="برنامه-نویسی")
        self.assertEqual(
            category.url,
            "/category/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3%DB%8C/",
        )
        self.assertEqual(self.client.get(category.url).status_code, 200)

    def test_article_count_only_counts_live_articles(self):
        category = create_category()
        create_article(slug="live", categories=[category])
        create_article(slug="draft", live=False, categories=[category])
        self.assertEqual(category.article_count(), 1)


class AuthorTests(TestCase):
    def test_url_points_to_index_route(self):
        author = create_author()
        self.assertEqual(author.url, "/author/sara/")

    def test_social_links_skips_empty_fields(self):
        author = create_author(website="https://example.com")
        self.assertEqual(author.social_links, [("وب‌سایت", "https://example.com")])

    def test_article_count(self):
        author = create_author()
        create_article(slug="one", author=author)
        self.assertEqual(author.article_count(), 1)
