from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import Truncator, slugify

from apps.core.models import Notification
from apps.core.translations import translate_lazy as _

# ACDNews and ACDNotes share one editorial model: the admin writes a single
# Post and picks which channel it's published to.
#   - channel == CHANNEL_NEWS: category is one of Sports / Economy /
#     Politics / Society, source_name/source_url are relevant, and any
#     remaining tags show under the post.
#   - channel == CHANNEL_NOTES: no source/category, just the post content
#     about the site itself (updates, new features).

CHANNEL_NEWS = 'news'
CHANNEL_NOTES = 'notes'
CHANNEL_CHOICES = [
    (CHANNEL_NEWS, 'ACDNews'),
    (CHANNEL_NOTES, 'ACDNotes'),
]

CATEGORY_SPORTS = 'sports'
CATEGORY_ECONOMY = 'economy'
CATEGORY_POLITICS = 'politics'
CATEGORY_SOCIETY = 'society'
# NOTE: these labels are deliberately kept as plain (not translate_lazy)
# strings — CATEGORY_KEYWORDS below needs them as plain hashable strings to
# match against raw tag text in Post.save(), and choices= values are used
# as dict keys/lookups elsewhere too (same reason PAGE_CHOICES/
# STAGE_CHOICES in apps/shop/models.py are plain strings). The public
# pages already display these correctly in both languages via
# {% t post.get_category_display %} (see templates/blog/*.html).
CATEGORY_CHOICES = [
    (CATEGORY_SPORTS, 'ورزشی'),
    (CATEGORY_ECONOMY, 'اقتصادی'),
    (CATEGORY_POLITICS, 'سیاسی'),
    (CATEGORY_SOCIETY, 'اجتماعی'),
]
# A small icon per section, used by the ACDNews filter pills.
CATEGORY_ICONS = {
    CATEGORY_SPORTS: 'trophy',
    CATEGORY_ECONOMY: 'graph-up-arrow',
    CATEGORY_POLITICS: 'bank',
    CATEGORY_SOCIETY: 'people',
}
# Reverse lookup (Persian label -> machine key) used to auto-detect a
# section from the raw tags text: if the admin types one of these four
# exact words as a tag, Post.save() below removes it from the tag list and
# uses it as the category instead (unless a category was already picked
# directly).
CATEGORY_KEYWORDS = {label: key for key, label in CATEGORY_CHOICES}


class Post(models.Model):
    channel = models.CharField(
        _('کانال انتشار'), max_length=10, choices=CHANNEL_CHOICES, default=CHANNEL_NEWS,
    )
    # Shared by both channels on purpose: an urgent ACDNotes update (e.g. "the
    # site is down") is just as real as an urgent ACDNews story. Ordering
    # (home page + both channel views) always sorts this first regardless of
    # published_at — see '-is_urgent' in the .order_by() calls in
    # apps/core/views.py and apps/blog/views.py.
    is_urgent = models.BooleanField(
        _('خبر فوری'),
        default=False,
        help_text=(
            'برای ACDNews و ACDNotes هر دو. پست فوری همیشه اول لیست می‌آید '
            '(بدون توجه به تاریخ انتشار) و با قاب/برچسب قرمز مشخص می‌شود.'
        ),
    )
    category = models.CharField(
        _('بخش خبری'),
        max_length=20, choices=CATEGORY_CHOICES, blank=True,
        help_text='فقط برای ACDNews. اگر خالی بماند و یکی از این چهار کلمه در تگ‌ها باشد، خودکار تشخیص داده می‌شود.',
    )

    title = models.CharField(_('عنوان'), max_length=220)
    slug = models.SlugField(_('نامک'), max_length=250, unique=True, blank=True, allow_unicode=True)

    summary = models.TextField(
        _('خلاصه'), blank=True, help_text='اگر خالی بماند، از ابتدای متن ساخته می‌شود.',
    )
    body = models.TextField(_('متن کامل'))

    tags = models.CharField(
        _('تگ‌ها'),
        max_length=300, blank=True,
        help_text='با کاما جدا کنید. کلمات ورزشی/اقتصادی/سیاسی/اجتماعی خودکار از این لیست حذف و به دسته تبدیل می‌شوند.',
    )
    source_name = models.CharField(_('نام منبع'), max_length=120, blank=True, help_text='فقط برای ACDNews')
    source_url = models.URLField(_('لینک منبع'), blank=True, help_text='فقط برای ACDNews')

    image = models.ImageField(_('تصویر'), upload_to='posts/', blank=True, null=True)
    image_url = models.URLField(
        _('لینک تصویر'),
        blank=True,
        help_text='لینک عکس خارجی (اگر عکسی آپلود نشود، از همین لینک استفاده می‌شود)',
    )

    is_active = models.BooleanField(_('فعال'), default=True)
    published_at = models.DateTimeField(_('تاریخ انتشار'), default=timezone.now)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('پست')
        verbose_name_plural = _('پست‌ها')
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.tags:
            items = [t.strip() for t in self.tags.split(',') if t.strip()]
            remaining = []
            detected = None
            for item in items:
                key = CATEGORY_KEYWORDS.get(item)
                if key:
                    detected = detected or key
                else:
                    remaining.append(item)
            if detected and not self.category:
                self.category = detected
            self.tags = ', '.join(remaining)

        if not self.slug:
            base = slugify(self.title, allow_unicode=True) or 'post'
            slug = base
            n = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f'{base}-{n}'
            self.slug = slug

        # Same "peek at the DB before overwriting" trick as Order.save() —
        # need to know whether is_urgent is newly True, not just currently
        # True, so editing an already-urgent post later doesn't re-notify
        # every single user again.
        was_urgent = False
        if self.pk:
            was_urgent = bool(Post.objects.filter(pk=self.pk).values_list('is_urgent', flat=True).first())

        super().save(*args, **kwargs)

        if self.is_urgent and self.is_active and not was_urgent:
            User = get_user_model()
            Notification.objects.bulk_create([
                Notification(
                    user=user,
                    message=f'{self.channel_label} · خبر فوری: {self.title}',
                    link=self.get_absolute_url(),
                )
                for user in User.objects.filter(is_active=True)
            ])

    @property
    def display_image(self):
        """Prefer an uploaded photo; fall back to the external image_url
        placeholder — same dual-field pattern as Product."""
        if self.image:
            return self.image.url
        return self.image_url

    @property
    def display_summary(self):
        return self.summary or Truncator(self.body).words(28, truncate=' …')

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    @property
    def channel_label(self):
        return 'ACDNews' if self.channel == CHANNEL_NEWS else 'ACDNotes'

    def get_absolute_url(self):
        name = 'blog:news_detail' if self.channel == CHANNEL_NEWS else 'blog:notes_detail'
        return reverse(name, args=[self.slug])
