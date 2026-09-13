# راهنمای تغییر ظاهر بلاگ (برای تیم فرانت)

هدف این ساختار یک چیز است: **بشود ظاهر بلاگ را در هر پروژه عوض کرد بدون اینکه
کسی به کد پایتون دست بزند.**

---

## سه فایل CSS، سه مسئولیت

قالب `templates/base.html` این سه فایل را به همین ترتیب بارگذاری می‌کند:

| فایل | مسئولیت | چقدر دست بزنیم |
| --- | --- | --- |
| `static/css/theme.css` | فقط **مقدارها**: رنگ، فونت، فاصله، گوشه، سایه، عرض | ✅ اولین و معمولاً تنها جایی که باید عوض شود |
| `static/css/blog.css` | **ساختار و چیدمان**. هیچ رنگ یا فونت ثابتی ندارد و فقط از توکن‌های بالا استفاده می‌کند | فقط وقتی چیدمان باید عوض شود |
| `static/css/custom.css` | بازنویسی‌های خاص همین پروژه. آخر از همه لود می‌شود، پس همیشه برنده است | ✅ برای چیزهای خاص و `@font-face` |

چون ترتیب بارگذاری این‌طور است، هر چیزی در `custom.css` بنویسید بر دوتای دیگر
اولویت دارد و لازم نیست `!important` بزنید.

---

## سناریوی ۱: فقط رنگ و فونت برند عوض شود

در `static/css/theme.css` دنبال بلوک `:root` بگردید:

```css
:root {
  --color-primary: #2563eb;        /* ← رنگ برند */
  --color-primary-hover: #1d4ed8;
  --color-primary-soft: #eff4ff;   /* پس‌زمینه‌ی ملایم هم‌خانواده */
  --color-on-primary: #ffffff;     /* متن روی رنگ برند */
  --color-accent: #0d9488;

  --font-sans: Vazirmatn, "IRANSansX", "Segoe UI", Tahoma, system-ui, sans-serif;
}
```

همین. دکمه‌ها، لینک‌ها، تگ‌ها، حاشیه‌ی مقاله‌ی ویژه و … همگی از همین توکن‌ها
می‌خوانند.

> اگر نمی‌خواهید `theme.css` را در گیت تغییر بدهید، همان چند خط را در
> `custom.css` بنویسید؛ نتیجه یکی است.

---

## سناریوی ۲: فونت اختصاصی

۱. فایل فونت را در `static/fonts/` بگذارید.
۲. در `static/css/custom.css`:

```css
@font-face {
  font-family: "Vazirmatn";
  src: url("../fonts/Vazirmatn-Regular.woff2") format("woff2");
  font-weight: 400;
  font-display: swap;
}
@font-face {
  font-family: "Vazirmatn";
  src: url("../fonts/Vazirmatn-Bold.woff2") format("woff2");
  font-weight: 700;
  font-display: swap;
}

:root {
  --font-sans: "Vazirmatn", system-ui, sans-serif;
}
```

فونت را از CDN نگیرید؛ فایل محلی هم سریع‌تر است هم مشکل تحریم ندارد.

> ⚠ فایل فونتی که در `url()` می‌نویسید باید واقعاً وجود داشته باشد. اگر نباشد،
> `collectstatic` هنگام استقرار با خطای `MissingFileError` متوقف می‌شود.

---

## سناریوی ۳: تغییر چیدمان

مثال‌های رایج، همه از راه توکن:

```css
:root {
  --container-width: 1320px;        /* صفحه پهن‌تر */
  --container-narrow-width: 680px;  /* ستون متن مقاله باریک‌تر */
  --card-min-width: 380px;          /* کارت‌های بزرگ‌تر → ستون کمتر */
  --cover-aspect-ratio: 4 / 3;      /* نسبت تصویر شاخص */
  --radius-md: 0;                   /* گوشه‌های تیز */
}
```

اگر چیدمان اساسی‌تری می‌خواهید، کلاس‌ها را در `blog.css` ببینید و در
`custom.css` بازنویسی کنید.

---

## سناریوی ۴: تغییر خود HTML

همه‌ی قالب‌ها در پوشه‌ی `templates/` هستند و چون این پوشه اول از همه در
مسیر جست‌وجوی قالب‌ها قرار دارد، می‌توانید آزادانه ویرایششان کنید:

```
templates/
  base.html                     اسکلت صفحه، متاتگ‌ها، بارگذاری CSS
  blog/
    blog_index_page.html        فهرست مقالات
    article_page.html           صفحه‌ی مقاله
    category_list.html          فهرست دسته‌بندی‌ها
    category_detail.html        مقالات یک دسته‌بندی
    author_list.html            فهرست نویسندگان
    author_detail.html          مقالات یک نویسنده
    includes/
      header.html               سربرگ و منو
      footer.html               پاورقی
      article_card.html         کارت مقاله (در همه‌ی فهرست‌ها استفاده می‌شود)
      pagination.html           صفحه‌بندی
    blocks/                     قالب هر بلوک بدنه‌ی مقاله
```

`base.html` این بلوک‌ها را برای بازنویسی در اختیار می‌گذارد:
`title`، `title_suffix`، `meta_description`، `canonical_url`، `social_meta`،
`extra_css`، `body_class`، `header`، `content`، `footer`، `extra_js`.

---

## چیزهایی که از پنل عوض می‌شوند (نه از کد)

اینها را ادمین محتوا در پنل، زیر **تنظیمات ← تنظیمات بلاگ** تغییر می‌دهد:

نام بلاگ، شعار، لوگو، فاوآیکون، تصویر پیش‌فرض اشتراک‌گذاری، متن پاورقی،
لینک سایت اصلی، لینک شبکه‌های اجتماعی.

پس برای عوض کردن لوگو لازم نیست کدی push شود.

---

## فیلترهای قالب که ممکن است لازمتان شود

```django
{% load blog_tags %}

{{ article.publish_date|jalali }}           {# ۲۲ شهریور ۱۴۰۴ #}
{{ article.publish_date|jalali:"short" }}   {# ۲۲ شهریور #}
{{ article.publish_date|jalali:"numeric" }} {# ۱۴۰۴/۰۶/۲۲ #}
{{ article.publish_date|iso_date }}         {# برای ویژگی datetime تگ <time> #}
{{ article.reading_time|persian_digits }}   {# ۵ #}

{% all_categories as categories %}
{% all_authors as authors %}
```

---

## حالت تیره

`theme.css` یک بلوک `@media (prefers-color-scheme: dark)` دارد که فقط مقدار
توکن‌ها را عوض می‌کند. اگر پروژه‌ای حالت تیره نمی‌خواهد، در `custom.css`
همان توکن‌ها را داخل همان مدیا-کوئری به مقادیر روشن برگردانید.

---

## نکته‌های راست‌به‌چپ

- صفحه `dir="rtl"` است. در CSS به‌جای `left/right` از خصوصیت‌های منطقی استفاده
  کنید: `margin-inline-start`، `border-inline-start`، `inset-inline-start`.
  آن‌وقت اگر روزی نسخه‌ی انگلیسی لازم شد، چیزی نمی‌شکند.
- `--leading-normal` عمداً `1.8` است؛ متن فارسی به فاصله‌ی خطی بازتر نیاز دارد.
- بلوک کد `dir="ltr"` دارد و نباید تغییر کند.

---

## بعد از تغییر

```bash
python manage.py runserver          # در توسعه کافی است
python manage.py collectstatic      # قبل از استقرار
```

فایل‌های استاتیک در پروداکشن hash دار می‌شوند (WhiteNoise)، پس کش مرورگر
کاربر به‌صورت خودکار باطل می‌شود.
