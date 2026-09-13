"""صفحه‌ی پیش‌فرض Wagtail را با «فهرست مقالات» جایگزین می‌کند."""

from django.db import migrations


def create_blog_index(apps, schema_editor):
    ContentType = apps.get_model("contenttypes.ContentType")
    Page = apps.get_model("wagtailcore.Page")
    Site = apps.get_model("wagtailcore.Site")
    BlogIndexPage = apps.get_model("blog.BlogIndexPage")

    # صفحه‌ی خوش‌آمدگویی پیش‌فرض Wagtail و سایت متصل به آن حذف می‌شوند.
    Site.objects.filter(is_default_site=True).delete()
    Page.objects.filter(id=2).delete()

    content_type, _ = ContentType.objects.get_or_create(
        model="blogindexpage", app_label="blog"
    )

    blog_index = BlogIndexPage.objects.create(
        title="بلاگ",
        draft_title="بلاگ",
        slug="blog",
        content_type=content_type,
        path="00010001",
        depth=2,
        numchild=0,
        url_path="/blog/",
        locale_id=1,
        articles_per_page=12,
    )

    root = Page.objects.get(depth=1)
    root.numchild = 1
    root.save(update_fields=["numchild"])

    Site.objects.create(
        hostname="localhost",
        port=80,
        site_name="بلاگ",
        root_page_id=blog_index.page_ptr_id,
        is_default_site=True,
    )


def remove_blog_index(apps, schema_editor):
    Page = apps.get_model("wagtailcore.Page")
    Site = apps.get_model("wagtailcore.Site")

    Site.objects.filter(is_default_site=True).delete()
    Page.objects.filter(slug="blog", depth=2).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
        ("wagtailcore", "0002_initial_data"),
    ]

    operations = [migrations.RunPython(create_blog_index, remove_blog_index)]
