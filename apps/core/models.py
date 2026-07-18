from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.translations import translate_lazy as _

# This app will host more site-wide, admin-managed content later:
#   - SiteSettings (logo, intro video/photos/text for the Home page)
#   - FooterLink (contact us / rules / Telegram / WhatsApp)
# Notification, Country and Representative are already here.


class Notification(models.Model):
    """
    In-site notification bell (not a real browser/OS push notification —
    that was considered and deliberately deferred: it needs a service
    worker + VAPID keys + a per-device permission prompt, real
    infrastructure this project doesn't have yet. This is the same idea
    without that: a bell icon in the header with an unread badge, only
    seen while actually on the site).

    Created automatically, never by hand in the admin:
      - apps.shop.models.Order.save() creates one for the order's own user
        whenever `stage` actually changes (progress OR regress).
      - apps.blog.models.Post.save() bulk-creates one per active user the
        moment a post's `is_urgent` flips from False to True (ACDNews or
        ACDNotes) — not on every subsequent save of an already-urgent post.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='notifications', verbose_name=_('کاربر'),
    )
    message = models.CharField(_('پیام'), max_length=255)
    # Internal path (e.g. /shop/orders/12/ or /acdnews/some-slug/), not a
    # full URLField — always generated from get_absolute_url(), never
    # typed by hand.
    link = models.CharField(_('لینک'), max_length=255, blank=True)
    is_read = models.BooleanField(_('خوانده‌شده'), default=False)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('اعلان')
        verbose_name_plural = _('اعلان‌ها')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} · {self.message[:40]}'


class Country(models.Model):
    """
    One row per country in the header's "کشورها" dropdown (see
    templates/partials/header.html) — picking one takes the visitor to
    that country's own page: background, flag, national anthem,
    description. Fully admin-managed, like Product/Post: add, edit,
    reorder, or deactivate from /admin/, nothing hardcoded in templates.

    flag_image/background_image/anthem_audio each follow the same
    "uploaded file wins, external URL is the fallback" dual-field pattern
    already used by Product.image/image_url and Post.image/image_url —
    see display_flag/display_background/display_anthem below. Prefixed
    per-purpose (flag_*, background_*, anthem_*) instead of the bare
    image/image_url Product and Post use, since this model needs three
    separate media slots instead of one.

    background_image_url doubles as the answer to "what if a country has
    no background photo": if the real data doesn't include one, set this
    to a link for a beautiful, fitting photo of that country instead (see
    its help_text) — there's no separate flag for "has a real background
    vs. a substituted one", the field just holds whichever applies.

    anthem_audio_url also accepts a YouTube link, not just a direct audio
    file URL — some anthem sources are videos, not bare mp3s. See
    anthem_is_youtube for how templates/core/country_detail.html tells the
    two apart to embed the right player.
    """
    name = models.CharField(_('نام کشور'), max_length=100)
    slug = models.SlugField(_('نامک'), max_length=150, unique=True, blank=True, allow_unicode=True)

    flag_image = models.ImageField(_('پرچم'), upload_to='countries/flags/', blank=True, null=True)
    flag_image_url = models.URLField(
        _('لینک پرچم'),
        blank=True,
        help_text='لینک عکس خارجی پرچم (اگر عکسی آپلود نشود، از همین لینک استفاده می‌شود)',
    )

    background_image = models.ImageField(_('تصویر پس‌زمینه'), upload_to='countries/backgrounds/', blank=True, null=True)
    background_image_url = models.URLField(
        _('لینک تصویر پس‌زمینه'),
        blank=True,
        help_text=(
            'لینک عکس خارجی پس‌زمینه (اگر عکسی آپلود نشود، از همین لینک استفاده می‌شود). '
            'اگر این کشور تصویر پس‌زمینه‌ی مشخصی نداشت، یک تصویر زیبا و مرتبط با همان کشور اینجا قرار دهید.'
        ),
    )

    anthem_audio = models.FileField(_('سرود ملی (فایل صوتی)'), upload_to='countries/anthems/', blank=True, null=True)
    anthem_audio_url = models.URLField(
        _('لینک سرود ملی'),
        blank=True,
        help_text='لینک فایل صوتی خارجی یا ویدیوی یوتیوب سرود ملی (اگر فایلی آپلود نشود، از همین لینک استفاده می‌شود)',
    )

    description = models.TextField(_('توضیحات'), blank=True)

    # "کشور در یک نگاه" quick-facts strip, shown right at the top of the
    # country page next to/under the description — cheap to fill in for
    # every country (stable facts, no photo needed) and exactly the kind
    # of "بیشتر بگو راجع به این کشور" context a first-time visitor wants
    # before ever opening an accordion section below.
    capital = models.CharField(_('پایتخت'), max_length=100, blank=True)
    official_language = models.CharField(_('زبان رسمی'), max_length=150, blank=True)
    currency = models.CharField(_('واحد پول'), max_length=100, blank=True)
    calling_code = models.CharField(_('کد تلفن بین‌الملل'), max_length=10, blank=True, help_text='مثلاً +98')
    best_time_to_visit = models.CharField(
        _('بهترین فصل سفر'), max_length=150, blank=True,
        help_text='مثلاً «بهار و پاییز» یا «اکتبر تا مارس»',
    )

    # Season-by-season weather blurb, shown on the country page under the
    # quick-facts strip so a visitor can tell at a glance what to pack /
    # when to go, without needing a live weather-API integration (which
    # would need its own key + daily fetch just like exchange_rate.py —
    # not worth it for "what's it usually like there in July").
    weather_spring = models.TextField(_('آب‌وهوا در بهار'), blank=True)
    weather_summer = models.TextField(_('آب‌وهوا در تابستان'), blank=True)
    weather_autumn = models.TextField(_('آب‌وهوا در پاییز'), blank=True)
    weather_winter = models.TextField(_('آب‌وهوا در زمستان'), blank=True)

    is_active = models.BooleanField(_('فعال'), default=True)
    order = models.PositiveIntegerField(_('ترتیب'), default=0)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('کشور')
        verbose_name_plural = _('کشورها')
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Same disambiguation-loop pattern as Post.slug (apps/blog/models.py)
        # — generated once from the name and left alone after that, so an
        # admin editing the name later doesn't silently break links already
        # shared to this country's page.
        if not self.slug:
            base = slugify(self.name, allow_unicode=True) or 'country'
            slug = base
            n = 1
            while Country.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f'{base}-{n}'
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def display_flag(self):
        if self.flag_image:
            return self.flag_image.url
        return self.flag_image_url

    @property
    def display_background(self):
        if self.background_image:
            return self.background_image.url
        return self.background_image_url

    @property
    def display_anthem(self):
        if self.anthem_audio:
            return self.anthem_audio.url
        return self.anthem_audio_url

    @property
    def anthem_is_youtube(self):
        """Only meaningful for an anthem_audio_url link (an uploaded
        anthem_audio file is always a real playable audio file) — tells
        the template whether to embed a YouTube <iframe> instead of a
        plain <audio> tag."""
        url = self.display_anthem or ''
        return 'youtube.com' in url or 'youtu.be' in url

    @property
    def anthem_youtube_embed_url(self):
        """Only used when anthem_is_youtube is True. YouTube refuses to
        let its normal /watch?v=... page load inside an <iframe> — only
        the .../embed/VIDEO_ID form is embeddable — but a plain watch link
        (or a youtu.be short link) is exactly what anyone would actually
        paste into anthem_audio_url. Converts either shape into the
        embeddable form; passes an already-/embed/ URL through untouched,
        and falls back to the raw URL if the shape isn't recognized rather
        than raising."""
        url = self.display_anthem or ''
        if 'youtube.com/embed/' in url:
            return url
        video_id = None
        if 'youtu.be/' in url:
            video_id = url.rsplit('youtu.be/', 1)[-1].split('?')[0].split('&')[0]
        elif 'watch?v=' in url:
            video_id = url.split('watch?v=', 1)[-1].split('&')[0]
        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'
        return url

    def get_absolute_url(self):
        return reverse('core:country_detail', args=[self.slug])


class Representative(models.Model):
    """
    Header-managed representative profiles. Each representative belongs to
    one Country so their profile can reuse that country's background image
    and flag while still keeping the representative's own photo and contact
    details separate.
    """
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, related_name='representatives',
        verbose_name=_('کشور'),
    )
    first_name = models.CharField(_('نام'), max_length=80)
    last_name = models.CharField(_('نام خانوادگی'), max_length=100)
    slug = models.SlugField(_('نامک'), max_length=180, unique=True, blank=True, allow_unicode=True)
    photo = models.ImageField(_('عکس نماینده'), upload_to='representatives/photos/', blank=True, null=True)
    photo_url = models.URLField(
        _('لینک عکس نماینده'), blank=True,
        help_text='اگر عکس آپلود نشود، از این لینک استفاده می‌شود.',
    )
    phone = models.CharField(_('شماره تماس'), max_length=40, blank=True)
    email = models.EmailField(_('ایمیل'), blank=True)
    position = models.CharField(_('عنوان'), max_length=120, blank=True)
    bio = models.TextField(_('توضیحات'), blank=True)
    is_active = models.BooleanField(_('فعال'), default=True)
    order = models.PositiveIntegerField(_('ترتیب'), default=0)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('نماینده')
        verbose_name_plural = _('نماینده‌ها')
        ordering = ['order', 'id']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.full_name, allow_unicode=True) or 'representative'
            slug = base
            n = 1
            while Representative.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f'{base}-{n}'
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    @property
    def display_photo(self):
        if self.photo:
            return self.photo.url
        return self.photo_url

    def get_absolute_url(self):
        return reverse('core:representative_detail', args=[self.slug])


class Attraction(models.Model):
    """
    One tourist attraction/landmark on a Country's page — the
    "جاذبه‌های گردشگری" accordion section in templates/core/
    country_detail.html shows these as a card grid; clicking a card opens
    its own full page (templates/core/attraction_detail.html) with the
    photo and complete description. Fully admin-managed; same dual
    image-field pattern used everywhere else in this project
    (display_image prefers the uploaded file, falls back to the external
    URL) so a real photo can go up later without touching any code.
    """
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='attractions',
        verbose_name=_('کشور'),
    )
    name = models.CharField(_('نام جاذبه'), max_length=150)
    slug = models.SlugField(_('نامک'), max_length=180, blank=True, allow_unicode=True)
    summary = models.CharField(
        _('خلاصه‌ی کوتاه'), max_length=220, blank=True,
        help_text='یک جمله‌ی کوتاه، زیر عکس توی لیست جاذبه‌ها نشان داده می‌شود.',
    )
    description = models.TextField(_('توضیحات کامل'), blank=True)

    image = models.ImageField(_('عکس'), upload_to='attractions/', blank=True, null=True)
    image_url = models.URLField(
        _('لینک عکس'), blank=True,
        help_text='اگر عکسی آپلود نشود، از این لینک استفاده می‌شود.',
    )

    is_active = models.BooleanField(_('فعال'), default=True)
    order = models.PositiveIntegerField(_('ترتیب'), default=0)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('جاذبه‌ی گردشگری')
        verbose_name_plural = _('جاذبه‌های گردشگری')
        ordering = ['order', 'id']
        # Unique only WITHIN a country (two different countries can each
        # have an attraction slugged "old-bazaar" with no collision) —
        # get_absolute_url is always reached through the parent country's
        # own slug too, so this is enough.
        unique_together = [('country', 'slug')]

    def __str__(self):
        return f'{self.name} ({self.country})'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True) or 'attraction'
            slug = base
            n = 1
            while Attraction.objects.filter(country=self.country, slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f'{base}-{n}'
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url

    def get_absolute_url(self):
        return reverse('core:attraction_detail', args=[self.country.slug, self.slug])


TRAVEL_MODE_AIR = 'air'
TRAVEL_MODE_LAND = 'land'
TRAVEL_MODE_RAIL = 'rail'
TRAVEL_MODE_SEA = 'sea'
TRAVEL_MODE_CHOICES = [
    (TRAVEL_MODE_AIR, 'هوایی'),
    (TRAVEL_MODE_LAND, 'زمینی (جاده)'),
    (TRAVEL_MODE_RAIL, 'ریلی (قطار)'),
    (TRAVEL_MODE_SEA, 'دریایی'),
]
# Small icon per mode, used by the route calculator's result card (same
# idea as blog's CATEGORY_ICONS).
TRAVEL_MODE_ICONS = {
    TRAVEL_MODE_AIR: 'airplane',
    TRAVEL_MODE_LAND: 'truck',
    TRAVEL_MODE_RAIL: 'train-front',
    TRAVEL_MODE_SEA: 'water',
}


class TravelRoute(models.Model):
    """
    Answers "از کشور مبدا تا اینجا چقدر راهه؟" on a Country's own page:
    the visitor picks an origin country + a transport mode from two
    dropdowns (templates/core/country_detail.html's route calculator),
    and the matching row here — if one exists — shows distance/duration.
    destination_country is always the page currently being viewed;
    origin_country is whichever of the other countries this specific
    route starts from.

    Nothing here is computed/estimated automatically — real distances and
    travel times vary too much by actual route/airline/border crossing to
    guess reliably, so every row is a deliberate, real entry made from the
    admin. Fully populating this means up to (35 other countries x up to
    4 modes) rows per destination, added over time as real data is
    gathered; a country with zero rows yet simply shows no results in the
    calculator instead of a wrong guess.
    """
    origin_country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='routes_from',
        verbose_name=_('کشور مبدا'),
    )
    destination_country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='routes_to',
        verbose_name=_('کشور مقصد'),
    )
    mode = models.CharField(_('نوع مسیر'), max_length=10, choices=TRAVEL_MODE_CHOICES)
    distance_km = models.PositiveIntegerField(_('فاصله (کیلومتر)'), null=True, blank=True)
    duration_text = models.CharField(
        _('زمان تقریبی سفر'), max_length=100, blank=True,
        help_text='مثلاً «حدود ۲ ساعت و ۳۰ دقیقه پرواز مستقیم»',
    )
    notes = models.TextField(
        _('توضیحات اضافه'), blank=True,
        help_text='مثلاً نام شرکت‌های هواپیمایی، مرز مشترک، تعداد توقف و غیره.',
    )
    is_active = models.BooleanField(_('فعال'), default=True)

    class Meta:
        verbose_name = _('مسیر سفر')
        verbose_name_plural = _('مسیرهای سفر')
        ordering = ['destination_country', 'origin_country', 'mode']
        unique_together = [('origin_country', 'destination_country', 'mode')]

    def __str__(self):
        return f'{self.origin_country} → {self.destination_country} ({self.get_mode_display()})'


HOTEL_STAR_CHOICES = [
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]


class Hotel(models.Model):
    """
    A well-known hotel shown on a Country's page — the "هتل‌های معروف"
    accordion section in templates/core/country_detail.html lists these
    as a card grid (photo, star rating, city, short summary). Unlike
    Attraction, a hotel doesn't get its own detail page — the card itself
    is the whole presentation, with an optional external booking_url the
    card links out to (real booking flow is out of scope for this site;
    this is informational/marketing only, same spirit as the rest of the
    country page). Same dual image-field pattern as everywhere else in
    this project.
    """
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='hotels',
        verbose_name=_('کشور'),
    )
    name = models.CharField(_('نام هتل'), max_length=150)
    slug = models.SlugField(_('نامک'), max_length=180, blank=True, allow_unicode=True)
    city = models.CharField(_('شهر'), max_length=100, blank=True)
    address = models.CharField(
        _('آدرس'), max_length=255, blank=True,
        help_text='آدرس کامل هتل، توی صفحه‌ی جزئیات هتل نشان داده می‌شود.',
    )
    phone_number = models.CharField(
        _('شماره تماس'), max_length=50, blank=True,
        help_text='مثلاً ‎+98 21 1234 5678',
    )
    star_rating = models.PositiveSmallIntegerField(
        _('درجه‌ی ستاره'), choices=HOTEL_STAR_CHOICES, default=5,
    )
    summary = models.CharField(
        _('خلاصه‌ی کوتاه'), max_length=220, blank=True,
        help_text='یک جمله‌ی کوتاه، زیر عکس توی لیست هتل‌ها نشان داده می‌شود.',
    )
    description = models.TextField(_('توضیحات کامل'), blank=True)

    image = models.ImageField(_('عکس'), upload_to='hotels/', blank=True, null=True)
    image_url = models.URLField(
        _('لینک عکس'), blank=True,
        help_text='اگر عکسی آپلود نشود، از این لینک استفاده می‌شود.',
    )
    booking_url = models.URLField(
        _('لینک رزرو/اطلاعات بیشتر'), blank=True,
        help_text='اختیاری — اگر پر شود، کارت این هتل به این لینک متصل می‌شود.',
    )
    price_usd = models.DecimalField(
        _('قیمت تقریبی هر شب (دلار)'), max_digits=8, decimal_places=2,
        null=True, blank=True,
        help_text=(
            'قیمت تقریبیِ هر شب اقامت به دلار آمریکا — مبنای نمودار قیمت توی صفحه‌ی '
            'جزئیات هتل. چون این سایت درگاه رزرو واقعی ندارد، این یک تخمین شاخص است نه '
            'نرخ لحظه‌ای؛ نسخه‌ی تومانی نمودار با نرخ روز دلار (که هر روز خودکار به‌روز '
            'می‌شود) از همین عدد محاسبه می‌شود.'
        ),
    )

    is_active = models.BooleanField(_('فعال'), default=True)
    order = models.PositiveIntegerField(_('ترتیب'), default=0)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('هتل')
        verbose_name_plural = _('هتل‌های معروف')
        ordering = ['order', 'id']
        unique_together = [('country', 'slug')]

    def __str__(self):
        return f'{self.name} ({self.country})'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True) or 'hotel'
            slug = base
            n = 1
            while Hotel.objects.filter(country=self.country, slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f'{base}-{n}'
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:hotel_detail', args=[self.country.slug, self.slug])

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url
