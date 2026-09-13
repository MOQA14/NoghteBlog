"""
سفارشی‌سازی پنل مدیریت.

هدف: پنل فقط همان سه بخش موردنیاز را نشان بدهد — مقالات (صفحات)،
دسته‌بندی‌ها و نویسندگان — و بخش‌های بلااستفاده‌ی Wagtail دیده نشوند.
"""

from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from blog.models import Author, Category


@register_snippet
class CategoryViewSet(SnippetViewSet):
    model = Category
    icon = "tag"
    menu_label = "دسته‌بندی‌ها"
    menu_name = "categories"
    menu_order = 200
    add_to_admin_menu = True
    list_display = ["name", "slug", "article_count"]
    list_per_page = 50
    search_fields = ("name", "description")


@register_snippet
class AuthorViewSet(SnippetViewSet):
    model = Author
    icon = "user"
    menu_label = "نویسندگان"
    menu_name = "authors"
    menu_order = 210
    add_to_admin_menu = True
    list_display = ["name", "job_title", "article_count"]
    list_per_page = 50
    search_fields = ("name", "job_title", "bio")


# آیتم‌های منوی اصلی که در این پروژه کاربردی ندارند.
HIDDEN_MAIN_MENU_ITEMS = {"snippets", "reports", "help", "documents"}


@hooks.register("construct_main_menu")
def hide_unused_main_menu_items(request, menu_items):
    menu_items[:] = [
        item for item in menu_items if item.name not in HIDDEN_MAIN_MENU_ITEMS
    ]


# زیرمنوهای «تنظیمات» که لازم نیستند (گردش‌کار غیرفعال است).
HIDDEN_SETTINGS_MENU_ITEMS = {"workflows", "workflow-tasks", "collections"}


@hooks.register("construct_settings_menu")
def hide_unused_settings_menu_items(request, menu_items):
    menu_items[:] = [
        item for item in menu_items if item.name not in HIDDEN_SETTINGS_MENU_ITEMS
    ]
