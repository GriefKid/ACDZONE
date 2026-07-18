import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

STAGE_CHOICES = [
    ('submitted', 'ثبت درخواست'),
    ('verifying', 'استعلام مدارک'),
    ('docs_submitted', 'مدارک ارسال شد'),
    ('payment_info_sent', 'راهنمای پرداخت'),
    ('payment_submitted', 'پرداخت ثبت شد'),
    ('payment_confirmed', 'پرداخت تایید شد'),
    ('card_registered', 'ثبت کارت در بانک'),
    ('printing', 'در حال چاپ'),
    ('shipped', 'ارسال شده'),
    ('availability_confirmed', 'تایید ظرفیت و تاریخ'),
    ('ticket_issued', 'بلیط صادر شد'),
]


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('page', models.CharField(choices=[('acdpay', 'ACDPay'), ('acdballoons', 'ACDBallons')], max_length=20)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('name_fa', models.CharField(max_length=100, null=True)),
                ('name_en', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('title_fa', models.CharField(max_length=200, null=True)),
                ('title_en', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(blank=True)),
                ('description_fa', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('price', models.PositiveBigIntegerField(help_text='به تومان')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('image_url', models.URLField(blank=True, help_text='لینک عکس خارجی (اگر عکسی آپلود نشود، از همین لینک استفاده می‌شود)')),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(choices=STAGE_CHOICES, default='submitted', max_length=30)),
                ('full_name', models.CharField(max_length=150)),
                ('contact_number', models.CharField(help_text='شماره واتساپ/تلگرام/بله', max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('admin_note', models.TextField(blank=True, help_text='یادداشت داخلی تیم فروش/مالی — مشتری این را نمی‌بیند')),
                ('is_hidden', models.BooleanField(default=False, help_text='وقتی مشتری از «محصولات من» حذف می‌کند، رکورد پاک نمی‌شود؛ فقط مخفی می‌شود')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
