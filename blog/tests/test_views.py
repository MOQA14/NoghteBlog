from django.conf import settings
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
from wagtail.admin.menu import admin_menu

from blog.tests.factories import create_article, create_author, create_category


class PublicPageTests(TestCase):
    def setUp(self):
        self.category = create_category()
        self.author = create_author()
        self.article = create_article(
            title="شروع کار با ویجتیل",
            slug="wagtail-intro",
            author=self.author,
            categories=[self.category],
        )

    def test_index_lists_articles(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "شروع کار با ویجتیل")

    def test_article_detail_renders(self):
        response = self.client.get(self.article.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "متن آزمایشی مقاله")
        self.assertContains(response, self.author.name)

    def test_category_detail_lists_its_articles(self):
        response = self.client.get("/category/python/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "شروع کار با ویجتیل")

    def test_unknown_category_returns_404(self):
        self.assertEqual(self.client.get("/category/nope/").status_code, 404)

    def test_category_list_page(self):
        response = self.client.get("/category/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_author_detail_lists_its_articles(self):
        response = self.client.get("/author/sara/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "شروع کار با ویجتیل")

    def test_unknown_author_returns_404(self):
        self.assertEqual(self.client.get("/author/nope/").status_code, 404)

    def test_author_list_page(self):
        response = self.client.get("/author/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.name)

    def test_search_filters_articles(self):
        create_article(title="مطلبی دیگر", slug="another")
        response = self.client.get("/", {"q": "ویجتیل"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "شروع کار با ویجتیل")

    def test_draft_article_is_not_public(self):
        draft = create_article(title="پیش‌نویس", slug="draft", live=False)
        self.assertEqual(self.client.get(draft.url).status_code, 404)


class PaginationTests(TestCase):
    def test_second_page_is_reachable(self):
        for number in range(15):
            create_article(title=f"مقاله {number}", slug=f"article-{number}")
        response = self.client.get("/", {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["articles"].object_list), 3)


class InfrastructureTests(TestCase):
    def test_rss_feed(self):
        create_article()
        response = self.client.get("/feed/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "اولین مقاله")

    def test_sitemap(self):
        create_article()
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/first-article/")

    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sitemap:")

    def test_admin_login_page_is_reachable(self):
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 200)

    def test_api_returns_articles(self):
        create_article()
        response = self.client.get("/api/v2/pages/", {"type": "blog.ArticlePage"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["meta"]["total_count"], 1)


class AdminTests(TestCase):
    """پنل فقط باید بخش‌های موردنیاز این پروژه را نشان بدهد."""

    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "pass1234!")
        self.client.force_login(User.objects.get(username="admin"))

    def _main_menu_names(self):
        request = RequestFactory().get("/admin/")
        request.user = User.objects.get(username="admin")
        return [item.name for item in admin_menu.menu_items_for_request(request)]

    def test_categories_and_authors_have_their_own_menu_items(self):
        names = self._main_menu_names()
        self.assertIn("categories", names)
        self.assertIn("authors", names)

    def test_unused_sections_are_hidden_from_the_menu(self):
        names = self._main_menu_names()
        for hidden in ("documents", "snippets", "reports", "help"):
            self.assertNotIn(hidden, names)

    def test_form_and_redirect_apps_are_not_installed(self):
        self.assertNotIn("wagtail.contrib.forms", settings.INSTALLED_APPS)
        self.assertNotIn("wagtail.contrib.redirects", settings.INSTALLED_APPS)

    def test_dashboard_renders(self):
        self.assertEqual(self.client.get("/admin/").status_code, 200)

    def test_category_and_author_listings_render(self):
        create_category()
        create_author()
        for url_name in ("wagtailsnippets_blog_category:list", "wagtailsnippets_blog_author:list"):
            with self.subTest(url_name=url_name):
                self.assertEqual(self.client.get(reverse(url_name)).status_code, 200)

    def test_workflow_is_disabled(self):
        self.assertFalse(settings.WAGTAIL_WORKFLOW_ENABLED)
