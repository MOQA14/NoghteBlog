"""بلوک‌های محتوایی بدنه‌ی مقاله (StreamField)."""

from django.conf import settings
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock


class HeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(label="متن سرتیتر", required=True)
    level = blocks.ChoiceBlock(
        label="سطح",
        choices=[("h2", "سرتیتر ۲"), ("h3", "سرتیتر ۳"), ("h4", "سرتیتر ۴")],
        default="h2",
    )

    class Meta:
        icon = "title"
        label = "سرتیتر"
        template = "blog/blocks/heading_block.html"


class FigureBlock(blocks.StructBlock):
    """تصویر همراه با زیرنویس. متن جایگزین (alt) روی خود تصویر تنظیم می‌شود."""

    image = ImageBlock(label="تصویر", required=True)
    caption = blocks.CharBlock(label="زیرنویس", required=False)

    class Meta:
        icon = "image"
        label = "تصویر"
        template = "blog/blocks/figure_block.html"


class QuoteBlock(blocks.StructBlock):
    text = blocks.TextBlock(label="متن نقل‌قول", required=True)
    attribution = blocks.CharBlock(label="گوینده / منبع", required=False)

    class Meta:
        icon = "openquote"
        label = "نقل‌قول"
        template = "blog/blocks/quote_block.html"


class CalloutBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(
        label="نوع",
        choices=[
            ("note", "نکته"),
            ("tip", "پیشنهاد"),
            ("warning", "هشدار"),
        ],
        default="note",
    )
    title = blocks.CharBlock(label="عنوان", required=False)
    text = blocks.RichTextBlock(
        label="متن", features=["bold", "italic", "link", "ol", "ul"]
    )

    class Meta:
        icon = "help"
        label = "کادر نکته"
        template = "blog/blocks/callout_block.html"


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(
        label="زبان",
        choices=[
            ("plain", "متن ساده"),
            ("python", "Python"),
            ("javascript", "JavaScript"),
            ("html", "HTML"),
            ("css", "CSS"),
            ("bash", "Bash"),
            ("sql", "SQL"),
            ("json", "JSON"),
            ("yaml", "YAML"),
        ],
        default="plain",
    )
    code = blocks.TextBlock(label="کد")

    class Meta:
        icon = "code"
        label = "قطعه کد"
        template = "blog/blocks/code_block.html"


class ArticleBodyBlock(blocks.StreamBlock):
    """بدنه‌ی مقاله."""

    paragraph = blocks.RichTextBlock(
        label="متن",
        features=settings.RICH_TEXT_FEATURES,
        template="blog/blocks/paragraph_block.html",
    )
    heading = HeadingBlock()
    image = FigureBlock()
    quote = QuoteBlock()
    callout = CalloutBlock()
    code = CodeBlock()
    embed = EmbedBlock(
        label="ویدیو / امبد",
        icon="media",
        template="blog/blocks/embed_block.html",
        help_text="نشانی ویدیو (آپارات، یوتیوب و ...) را بگذارید.",
    )
    html = blocks.RawHTMLBlock(
        label="کد HTML (پیشرفته)",
        icon="code",
        help_text="فقط برای مواقع لازم؛ محتوای این بلوک بدون فیلتر نمایش داده می‌شود.",
    )

    class Meta:
        block_counts = {}
