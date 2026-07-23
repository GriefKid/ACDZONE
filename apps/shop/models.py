from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.core.models import Notification
from apps.core.translations import translate_lazy as _

# ACDPay and ACDBallons are the same underlying structure (a category of
# products with a buy button that creates an order visible on "My
# Products"), just with different catalog items and different order-stage
# flows — cards need bank registration + printing, balloon tickets don't.
# See README for the full sales-process background.

PAGE_ACDPAY = 'acdpay'
PAGE_ACDBALLOONS = 'acdballoons'

PAGE_CHOICES = [
    (PAGE_ACDPAY, 'ACDPay'),
    (PAGE_ACDBALLOONS, 'ACDBallons'),
]

SERVICE_IMAGE_PATHS = {
    'یونیون‌کارت': 'img/services/unioncard.svg',
    'ویزاکارت': 'img/services/visacard.svg',
    'بالن‌سواری آب‌سرد': 'img/services/balloon-absard.svg',
    'بالن‌سواری احمدآباد مستوفی': 'img/services/balloon-ahmadabad.svg',
}

# Every stage that exists anywhere, keyed by a stable machine name. Several
# keys are shared between both flows below because they mean the same thing
# for cards and tickets alike (submitted / payment_info_sent / etc.).
STAGE_LABELS = {
    'submitted': 'ثبت درخواست',
    'verifying': 'استعلام مدارک',
    'docs_submitted': 'مدارک ارسال شد',
    'payment_info_sent': 'راهنمای پرداخت',
    'payment_submitted': 'پرداخت ثبت شد',
    'payment_confirmed': 'پرداخت تایید شد',
    'card_registered': 'ثبت کارت در بانک',
    'printing': 'در حال چاپ',
    'shipped': 'ارسال شده',
    'availability_confirmed': 'تایید ظرفیت و تاریخ',
    'ticket_issued': 'بلیط صادر شد',
}

# The ACDPay sales process (manual, human-in-the-loop via WhatsApp/Telegram/
# Bale between customer, sales manager, and finance manager). Confirmed with
# the site owner: ends at "shipped" — no separate customer-confirmed
# "delivered" stage for now.
ACDPAY_STAGE_FLOW = [
    'submitted',
    'verifying',
    'docs_submitted',
    'payment_info_sent',
    'payment_submitted',
    'payment_confirmed',
    'card_registered',
    'printing',
    'shipped',
]

# ACDBallons orders: simpler flow, no bank registration or printing since
# there's no physical card involved. Confirmed with the site owner: 6
# stages, ending at "ticket_issued".
ACDBALLOONS_STAGE_FLOW = [
    'submitted',
    'availability_confirmed',
    'payment_info_sent',
    'payment_submitted',
    'payment_confirmed',
    'ticket_issued',
]

STAGE_FLOWS_BY_PAGE = {
    PAGE_ACDPAY: ACDPAY_STAGE_FLOW,
    PAGE_ACDBALLOONS: ACDBALLOONS_STAGE_FLOW,
}

# Union of both flows, for the Order.stage model field's `choices=`. Django
# doesn't support choices that depend on another field's value, so both
# flows' keys are offered here; get_stage_progress() below is what actually
# enforces the correct sequence/subset for a given order's category.
STAGE_CHOICES = [(key, label) for key, label in STAGE_LABELS.items()]


class Category(models.Model):
    name = models.CharField(_('نام'), max_length=100)
    page = models.CharField(_('صفحه'), max_length=20, choices=PAGE_CHOICES)
    order = models.PositiveIntegerField(_('ترتیب'), default=0)
    is_active = models.BooleanField(_('فعال'), default=True)

    class Meta:
        verbose_name = _('دسته‌بندی')
        verbose_name_plural = _('دسته‌بندی‌ها')
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

    def stage_flow(self):
        return STAGE_FLOWS_BY_PAGE.get(self.page, ACDPAY_STAGE_FLOW)


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products', verbose_name=_('دسته‌بندی'),
    )
    title = models.CharField(_('عنوان'), max_length=200)
    # Short: previews, carousel captions, product cards. Long: full-length
    # copy for a product's own detail/info section — same content, two
    # lengths, used in different spots (see apps/core/translations.py-style
    # per-context reuse pattern, just for DB content instead of static UI text).
    description = models.TextField(_('توضیح کوتاه'), blank=True)
    long_description = models.TextField(_('توضیح کامل'), blank=True)
    price = models.PositiveBigIntegerField(_('قیمت'), help_text='به تومان')
    image = models.ImageField(_('تصویر'), upload_to='products/', blank=True, null=True)
    image_url = models.URLField(
        _('لینک تصویر'),
        blank=True,
        help_text='لینک عکس خارجی (اگر عکسی آپلود نشود، از همین لینک استفاده می‌شود)',
    )
    is_active = models.BooleanField(_('فعال'), default=True)
    order = models.PositiveIntegerField(_('ترتیب'), default=0)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        service_image = SERVICE_IMAGE_PATHS.get(self.title_fa)
        if service_image:
            return f'{settings.STATIC_URL.rstrip("/")}/{service_image}'
        if self.image:
            return self.image.url
        return self.image_url

    @property
    def url_name(self):
        """Matches the {% url %} name used by templates/core/home.html's
        product carousel — 'shop:acdpay' or 'shop:acdballoons' — since
        Category.page's stored values are exactly those url-name suffixes."""
        return f'shop:{self.category.page}'


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name=_('کاربر'),
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orders', verbose_name=_('محصول'),
    )
    stage = models.CharField(_('مرحله'), max_length=30, choices=STAGE_CHOICES, default='submitted')
    full_name = models.CharField(_('نام و نام خانوادگی'), max_length=150)
    contact_number = models.CharField(
        _('شماره تماس'), max_length=30, help_text='شماره واتساپ/تلگرام/بله',
    )
    email = models.EmailField(_('ایمیل'), blank=True)
    admin_note = models.TextField(
        _('یادداشت داخلی'), blank=True, help_text='یادداشت داخلی تیم فروش/مالی — مشتری این را نمی‌بیند',
    )
    is_hidden = models.BooleanField(
        _('مخفی از مشتری'),
        default=False, help_text='وقتی مشتری از «محصولات من» حذف می‌کند، رکورد پاک نمی‌شود؛ فقط مخفی می‌شود',
    )
    created_at = models.DateTimeField(_('تاریخ ثبت'), auto_now_add=True)
    updated_at = models.DateTimeField(_('آخرین بروزرسانی'), auto_now=True)

    class Meta:
        verbose_name = _('سفارش')
        verbose_name_plural = _('سفارش‌ها')
        ordering = ['-created_at']

    def __str__(self):
        return f'#{self.pk} · {self.product.title} · {self.user}'

    def save(self, *args, **kwargs):
        # Fetch the stage as it currently is IN THE DATABASE, before this
        # save overwrites it — the only way to tell "did stage change" from
        # inside save() itself. Works whether the change came from the full
        # admin change form or a quick edit in list_editable, since both
        # ultimately call Order.save() on the instance.
        old_stage = None
        if self.pk:
            old_stage = Order.objects.filter(pk=self.pk).values_list('stage', flat=True).first()

        super().save(*args, **kwargs)

        if old_stage is not None and old_stage != self.stage:
            # Any direction counts — the customer cares just as much about a
            # regression (e.g. back to "verifying" because a document was
            # rejected) as a forward step.
            Notification.objects.create(
                user=self.user,
                message=f'وضعیت سفارش «{self.product.title}» به «{self.stage_label()}» تغییر کرد.',
                link=self.get_absolute_url(),
            )

    def stage_flow(self):
        return self.product.category.stage_flow()

    def stage_label(self):
        return STAGE_LABELS.get(self.stage, self.stage)

    def get_stage_progress(self):
        """Returns the ordered list of steps for this order's category,
        each tagged with its status relative to the order's current stage
        — done / current / pending — for the stepper UI."""
        flow = self.stage_flow()
        try:
            current_index = flow.index(self.stage)
        except ValueError:
            current_index = 0
        steps = []
        for i, key in enumerate(flow):
            if i < current_index:
                status = 'done'
            elif i == current_index:
                status = 'current'
            else:
                status = 'pending'
            steps.append({
                'key': key,
                'label': STAGE_LABELS[key],
                'status': status,
                'index': i + 1,
            })
        return steps

    def get_absolute_url(self):
        return reverse('shop:order_detail', args=[self.pk])
