from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام کشور')),
                ('name_fa', models.CharField(max_length=100, null=True, verbose_name='نام کشور')),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='نام کشور')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=150, unique=True, verbose_name='نامک')),
                ('flag_image', models.ImageField(blank=True, null=True, upload_to='countries/flags/', verbose_name='پرچم')),
                ('flag_image_url', models.URLField(
                    blank=True,
                    help_text='لینک عکس خارجی پرچم (اگر عکسی آپلود نشود، از همین لینک استفاده می‌شود)',
                    verbose_name='لینک پرچم',
                )),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='countries/backgrounds/', verbose_name='تصویر پس‌زمینه')),
                ('background_image_url', models.URLField(
                    blank=True,
                    help_text=(
                        'لینک عکس خارجی پس‌زمینه (اگر عکسی آپلود نشود، از همین لینک استفاده می‌شود). '
                        'اگر این کشور تصویر پس‌زمینه‌ی مشخصی نداشت، یک تصویر زیبا و مرتبط با همان کشور اینجا قرار دهید.'
                    ),
                    verbose_name='لینک تصویر پس‌زمینه',
                )),
                ('anthem_audio', models.FileField(blank=True, null=True, upload_to='countries/anthems/', verbose_name='سرود ملی (فایل صوتی)')),
                ('anthem_audio_url', models.URLField(
                    blank=True,
                    help_text='لینک فایل صوتی خارجی یا ویدیوی یوتیوب سرود ملی (اگر فایلی آپلود نشود، از همین لینک استفاده می‌شود)',
                    verbose_name='لینک سرود ملی',
                )),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('description_fa', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='ترتیب')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'کشور',
                'verbose_name_plural': 'کشورها',
                'ordering': ['order', 'id'],
            },
        ),
    ]
