# NoghteBlog

بلاگ مستقل مبتنی بر [Wagtail](https://wagtail.org) و جنگو.

این پروژه عمداً **کوچک** نگه داشته شده: از میان همه‌ی امکانات Wagtail فقط
سه چیز فعال است — **مقالات**، **دسته‌بندی‌ها** و **نویسندگان**.

---

## راه‌اندازی محلی

**پیش‌نیاز: پایتون ۳.۱۰ یا بالاتر** (Wagtail 8 و جنگو 5.2 پایین‌تر را پشتیبانی نمی‌کنند).

روی دبیان/اوبونتو اول این بسته‌ها را نصب کنید، وگرنه `python3 -m venv` کار نمی‌کند:

```bash
sudo apt update && sudo apt install -y python3-venv python3-full
```

```bash
python3 -m venv .venv
ls -l .venv/bin/python             # باید وجود داشته باشد؛ اگر نبود venv ساخته نشده

source .venv/bin/activate          # ویندوز: .venv\Scripts\activate
                                   # بعد از این باید (.venv) اول خط ترمینال بیاید
pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env               # اختیاری؛ بدونش هم اجرا می‌شود

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo         # اختیاری: محتوای نمونه برای تیم فرانت
python manage.py runserver
```

اگر نمی‌خواهید venv را فعال کنید، همه‌ی دستورها را با مسیر کامل بزنید:
`.venv/bin/pip` و `.venv/bin/python` به‌جای `pip` و `python`.

- بلاگ: <http://localhost:8000/>
- پنل مدیریت: <http://localhost:8000/admin/>

بدون `DATABASE_URL` از SQLite استفاده می‌شود، پس برای شروع به دیتابیس نیاز نیست.
تنظیمات پروژه یک فایل است: `config/settings.py`. تفاوت محیط‌ها فقط از
متغیرهای محیطی می‌آید و کلید اصلی `DEBUG` است.

### اگر بالا نیامد

| نشانه | علت و راه حل |
| --- | --- |
| `error: externally-managed-environment` | `pip` سیستمی را صدا زده‌اید، نه pip داخل venv. اول `source .venv/bin/activate` یا مستقیم `.venv/bin/pip install -r requirements.txt`. هرگز از `--break-system-packages` استفاده نکنید. |
| `Cannot run program ".venv/bin/python" ... No such file or directory` | venv ساخته نشده. `sudo apt install python3-venv python3-full` و بعد `python3 -m venv .venv`. |
| `ensurepip is not available` هنگام ساخت venv | بسته‌ی `python3-venv` نصب نیست (خطای رایج دبیان/اوبونتو). |
| `SyntaxError` هنگام نصب یا اجرا | پایتون قدیمی است. `python3 --version` باید ۳.۱۰ به بالا باشد. |
| `DisallowedHost` یا خطای ۴۰۰ | `DEBUG=false` است ولی `ALLOWED_HOSTS` دامنه‌ی درست را ندارد. برای کار لوکال در `.env` مقدار `DEBUG=true` بگذارید. |
| `ImproperlyConfigured: SECRET_KEY الزامی است` | `DEBUG=false` است و کلید داده نشده. برای کار لوکال `cp .env.example .env`. |
| `ModuleNotFoundError: wagtail` | محیط مجازی فعال نیست. `source .venv/bin/activate` |
| `no such table` | `python manage.py migrate` اجرا نشده. |
| صفحه‌ی اصلی ۴۰۴ می‌دهد | دیتابیس بدون مایگریشن `0002_create_blog_index` ساخته شده. `manage.py migrate` را کامل اجرا کنید. |
| خطای نصب `psycopg` | فقط برای PostgreSQL لازم است. برای کار لوکال با SQLite می‌توانید آن خط را از `requirements.txt` موقتاً بردارید. |

### PyCharm

بعد از ساخته شدن `.venv`، مفسر پروژه را دستی معرفی کنید:

`Settings → Project: NoghteBlog → Python Interpreter → Add Interpreter
→ Add Local Interpreter → Virtualenv Environment → Existing`

و مسیر `.venv/bin/python` داخل پوشه‌ی پروژه را انتخاب کنید.

برای اجرای سرور از داخل PyCharm، یک Run Configuration از نوع **Django Server**
بسازید (یا Python با اسکریپت `manage.py` و آرگومان `runserver`).

---

## چه چیزی هست و چه چیزی نیست

| هست | نیست |
| --- | --- |
| مقالات با پیش‌نویس/انتشار و تاریخچه‌ی نسخه‌ها | فرم‌ساز (`wagtail.contrib.forms`) |
| دسته‌بندی‌ها (Snippet) | ریدایرکت‌ها (`wagtail.contrib.redirects`) |
| نویسندگان (Snippet) | کتابخانه‌ی اسناد (از منو حذف شده) |
| کتابخانه‌ی تصاویر | گردش‌کار تأیید محتوا (`WAGTAIL_WORKFLOW_ENABLED = False`) |
| جست‌وجو، صفحه‌بندی، RSS، sitemap، robots | نتایج تبلیغاتی جست‌وجو |
| API فقط-خواندنی (اختیاری) | چندزبانه بودن |

> **چرا `wagtail.documents` نصب است؟** پنل مدیریت Wagtail ۸ وابستگی سخت به آن
> دارد و بدونش بالا نمی‌آید. در `blog/wagtail_hooks.py` از منو حذف شده و در
> ویرایشگر متن هم امکان درج سند فعال نیست.

---

## ساختار پروژه

```
config/                 تنظیمات، مسیرها، API
  settings.py           تنظیمات یکپارچه‌ی همه‌ی محیط‌ها
blog/
  models.py             ArticlePage, Category, Author, BlogIndexPage, BlogSettings
  blocks.py             بلوک‌های بدنه‌ی مقاله (StreamField)
  wagtail_hooks.py      سفارشی‌سازی پنل مدیریت
  feeds.py              خوراک RSS
  templatetags/         فیلترهای تاریخ شمسی و اعداد فارسی
  management/commands/  seed_demo
templates/              همه‌ی قالب‌های سمت کاربر
static/css/
  theme.css             ← توکن‌های طراحی (کار تیم فرانت)
  blog.css              ساختار و چیدمان
  custom.css            بازنویسی‌های اختصاصی پروژه
docs/THEMING.md         راهنمای تیم فرانت
```

---

## مدل محتوا

**مقاله (`ArticlePage`)** — زیرمجموعه‌ی «فهرست مقالات»
عنوان، اسلاگ، چکیده، تصویر شاخص، بدنه (StreamField)، نویسنده، دسته‌بندی‌ها،
تاریخ انتشار، مقاله‌ی ویژه. زمان مطالعه خودکار محاسبه می‌شود.

بلوک‌های بدنه: متن، سرتیتر، تصویر، نقل‌قول، کادر نکته، قطعه کد، ویدیو/امبد، HTML خام.

**دسته‌بندی (`Category`)** — نام، اسلاگ، توضیح، تصویر
**نویسنده (`Author`)** — نام، اسلاگ، عنوان شغلی، معرفی، تصویر، راه‌های ارتباطی،
اتصال اختیاری به یک کاربر پنل

**تنظیمات بلاگ (`BlogSettings`)** — در پنل زیر «تنظیمات»: نام بلاگ، شعار، لوگو،
فاوآیکون، تصویر اشتراک‌گذاری، پاورقی، لینک سایت اصلی، شبکه‌های اجتماعی.

---

## نشانی‌ها

| مسیر | توضیح |
| --- | --- |
| `/` | فهرست مقالات (با `?q=` جست‌وجو و `?page=` صفحه‌بندی) |
| `/<اسلاگ-مقاله>/` | صفحه‌ی مقاله |
| `/category/` | فهرست دسته‌بندی‌ها |
| `/category/<اسلاگ>/` | مقالات یک دسته‌بندی |
| `/author/` | فهرست نویسندگان |
| `/author/<اسلاگ>/` | مقالات یک نویسنده |
| `/feed/` | خوراک RSS |
| `/sitemap.xml` , `/robots.txt` | سئو |
| `/admin/` | پنل مدیریت |
| `/api/v2/pages/` | API فقط-خواندنی |

---

## API فقط-خواندنی

برای وقتی که یک پروژه‌ی دیگر بخواهد مقالات را داخل سایت خودش نشان بدهد:

```
GET /api/v2/pages/?type=blog.ArticlePage&fields=title,intro,cover_image,publish_date&limit=3
```

با `BLOG_API_ENABLED=false` در `.env` کاملاً خاموش می‌شود.

---

## تغییر ظاهر

تیم فرانت برای هر پروژه فقط `static/css/theme.css` (و در صورت نیاز
`static/css/custom.css`) را عوض می‌کند — بدون دست زدن به پایتون.
جزئیات در **[docs/THEMING.md](docs/THEMING.md)**.

---

## تست و لینت

```bash
python manage.py test blog
ruff check .
```

---

## استقرار

استقرار با **dokploy** و `Dockerfile` استاندارد شرکت انجام می‌شود.
`Dockerfile` دست‌نخورده است؛ `docker-compose.yml` با آن هماهنگ شده.

```bash
# متغیرهای الزامی (در dokploy تنظیم می‌شوند، نه در ریپو)
SECRET_KEY=...            # python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
ALLOWED_HOSTS=blog.example.com
POSTGRES_PASSWORD=...
```

اگر هر کدام نباشند، `docker compose` پیش از بالا آمدن با پیام صریح متوقف می‌شود.

### volume ها

| volume | مسیر | چرا لازم است |
| --- | --- | --- |
| `media_data` | `/app/media` | تصاویری که ادمین آپلود می‌کند. بدون آن، هر دیپلوی مجدد همه‌ی تصاویر را پاک می‌کند. |
| `postgres_data` | `/var/lib/postgresql/data` | داده‌های دیتابیس. |

`staticfiles` عمداً volume ندارد، چون `Dockerfile` در هر بار بالا آمدن
`collectstatic` را اجرا می‌کند و محتوایش بازساخته می‌شود.

### سه نکته‌ای که از روی همین Dockerfile تعیین شده‌اند

1. **`DEBUG=false` رفتار استقرار را فعال می‌کند.** تنظیمات یک فایل است و همه‌ی
   نقاط ورود همان را برمی‌دارند، پس `migrate` و `collectstatic` و gunicorn
   نمی‌توانند با تنظیمات متفاوت اجرا شوند. با `DEBUG=false` این‌ها روشن
   می‌شوند: الزامی شدن `SECRET_KEY` و `ALLOWED_HOSTS`، ریدایرکت HTTPS،
   کوکی امن، HSTS، و فایل‌های استاتیک hash دار.

2. **`.dockerignore` حیاتی است.** `Dockerfile` ماژول پروژه را با
   `find . -name wsgi.py | head -n 1` پیدا می‌کند. اگر `.venv` داخل ایمیج کپی
   شود، هفت `wsgi.py` دیگر هم پیدا می‌شود و ممکن است به‌جای `config` یکی از
   آن‌ها انتخاب شود.

3. **`depends_on` با `condition: service_healthy`.** چون `migrate` هنگام بالا
   آمدن کانتینر اجرا می‌شود، وب باید منتظر آماده شدن دیتابیس بماند.

### رمز دیتابیس

دیتابیس فقط داخل همین `docker-compose.yml` تعریف شده، پورتی روی هاست منتشر
نمی‌کند و تنها از شبکه‌ی داخلی compose در دسترس است. رمزی از قبل وجود ندارد —
خودتان می‌سازید و در تنظیمات محیطی dokploy می‌گذارید:

```bash
openssl rand -hex 32
```

`hex` عمداً پیشنهاد شده: خروجی‌اش فقط حروف و عدد است و در `DATABASE_URL`
مشکل‌ساز نمی‌شود. اگر از `base64` استفاده کنید ممکن است `+` یا `/` بیاید که
باید percent-encode شود.

> رمز را بعد از اولین دیپلوی عوض نکنید؛ دیتابیس آن را هنگام ساخت volume ذخیره
> می‌کند و تغییر بعدی باعث خطای احراز هویت می‌شود. برای تغییر واقعی باید رمز را
> داخل خود postgres هم عوض کنید.

### شبکه و دامنه

بسته به نسخه‌ی dokploy، دامنه یا از رابط کاربری تنظیم می‌شود یا با وصل شدن به
شبکه‌ی traefik. بخش مربوطه در انتهای `docker-compose.yml` کامنت شده؛ با مدیر
آی‌تی چک کنید کدام روش در شرکت شما استفاده می‌شود.

سرویس وب فقط `expose` دارد و پورتی روی هاست منتشر نمی‌کند، چون ترافیک از
traefik می‌آید. اگر بدون ریورس‌پروکسی تست می‌کنید، موقتاً `ports` اضافه کنید.

### بعد از اولین دیپلوی

```bash
docker compose exec web python manage.py createsuperuser
```

سپس در پنل، زیر **تنظیمات → سایت‌ها**، دامنه را از `localhost` به دامنه‌ی
واقعی تغییر دهید.
