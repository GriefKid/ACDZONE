import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_expand_tourism_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام هتل')),
                ('name_fa', models.CharField(max_length=150, null=True, verbose_name='نام هتل')),
                ('name_en', models.CharField(max_length=150, null=True, verbose_name='نام هتل')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='شهر')),
                ('city_fa', models.CharField(blank=True, max_length=100, null=True, verbose_name='شهر')),
                ('city_en', models.CharField(blank=True, max_length=100, null=True, verbose_name='شهر')),
                ('star_rating', models.PositiveSmallIntegerField(
                    choices=[(3, '★★★'), (4, '★★★★'), (5, '★★★★★')],
                    default=5, verbose_name='درجه‌ی ستاره',
                )),
                ('summary', models.CharField(
                    blank=True, max_length=220,
                    help_text='یک جمله‌ی کوتاه، زیر عکس توی لیست هتل‌ها نشان داده می‌شود.',
                    verbose_name='خلاصه‌ی کوتاه',
                )),
                ('summary_fa', models.CharField(
                    blank=True, max_length=220, null=True,
                    help_text='یک جمله‌ی کوتاه، زیر عکس توی لیست هتل‌ها نشان داده می‌شود.',
                    verbose_name='خلاصه‌ی کوتاه',
                )),
                ('summary_en', models.CharField(
                    blank=True, max_length=220, null=True,
                    help_text='یک جمله‌ی کوتاه، زیر عکس توی لیست هتل‌ها نشان داده می‌شود.',
                    verbose_name='خلاصه‌ی کوتاه',
                )),
                ('description', models.TextField(blank=True, verbose_name='توضیحات کامل')),
                ('description_fa', models.TextField(blank=True, null=True, verbose_name='توضیحات کامل')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='توضیحات کامل')),
                ('image', models.ImageField(blank=True, null=True, upload_to='hotels/', verbose_name='عکس')),
                ('image_url', models.URLField(
                    blank=True,
                    help_text='اگر عکسی آپلود نشود، از این لینک استفاده می‌شود.',
                    verbose_name='لینک عکس',
                )),
                ('booking_url', models.URLField(
                    blank=True,
                    help_text='اختیاری — اگر پر شود، کارت این هتل به این لینک متصل می‌شود.',
                    verbose_name='لینک رزرو/اطلاعات بیشتر',
                )),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='ترتیب')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('country', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='hotels',
                    to='core.country',
                    verbose_name='کشور',
                )),
            ],
            options={
                'verbose_name': 'هتل',
                'verbose_name_plural': 'هتل‌های معروف',
                'ordering': ['order', 'id'],
            },
        ),
    ]
