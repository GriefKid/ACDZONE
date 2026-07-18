import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_representative_name_translations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام جاذبه')),
                ('name_fa', models.CharField(max_length=150, null=True, verbose_name='نام جاذبه')),
                ('name_en', models.CharField(max_length=150, null=True, verbose_name='نام جاذبه')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=180, verbose_name='نامک')),
                ('summary', models.CharField(
                    blank=True, max_length=220,
                    help_text='یک جمله‌ی کوتاه، زیر عکس توی لیست جاذبه‌ها نشان داده می‌شود.',
                    verbose_name='خلاصه‌ی کوتاه',
                )),
                ('summary_fa', models.CharField(
                    blank=True, max_length=220, null=True,
                    help_text='یک جمله‌ی کوتاه، زیر عکس توی لیست جاذبه‌ها نشان داده می‌شود.',
                    verbose_name='خلاصه‌ی کوتاه',
                )),
                ('summary_en', models.CharField(
                    blank=True, max_length=220, null=True,
                    help_text='یک جمله‌ی کوتاه، زیر عکس توی لیست جاذبه‌ها نشان داده می‌شود.',
                    verbose_name='خلاصه‌ی کوتاه',
                )),
                ('description', models.TextField(blank=True, verbose_name='توضیحات کامل')),
                ('description_fa', models.TextField(blank=True, null=True, verbose_name='توضیحات کامل')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='توضیحات کامل')),
                ('image', models.ImageField(blank=True, null=True, upload_to='attractions/', verbose_name='عکس')),
                ('image_url', models.URLField(
                    blank=True,
                    help_text='اگر عکسی آپلود نشود، از این لینک استفاده می‌شود.',
                    verbose_name='لینک عکس',
                )),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='ترتیب')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('country', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='attractions',
                    to='core.country',
                    verbose_name='کشور',
                )),
            ],
            options={
                'verbose_name': 'جاذبه‌ی گردشگری',
                'verbose_name_plural': 'جاذبه‌های گردشگری',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='attraction',
            unique_together={('country', 'slug')},
        ),
        migrations.CreateModel(
            name='TravelRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(
                    choices=[
                        ('air', 'هوایی'),
                        ('land', 'زمینی (جاده)'),
                        ('rail', 'ریلی (قطار)'),
                        ('sea', 'دریایی'),
                    ],
                    max_length=10, verbose_name='نوع مسیر',
                )),
                ('distance_km', models.PositiveIntegerField(blank=True, null=True, verbose_name='فاصله (کیلومتر)')),
                ('duration_text', models.CharField(
                    blank=True, max_length=100,
                    help_text='مثلاً «حدود ۲ ساعت و ۳۰ دقیقه پرواز مستقیم»',
                    verbose_name='زمان تقریبی سفر',
                )),
                ('duration_text_fa', models.CharField(
                    blank=True, max_length=100, null=True,
                    help_text='مثلاً «حدود ۲ ساعت و ۳۰ دقیقه پرواز مستقیم»',
                    verbose_name='زمان تقریبی سفر',
                )),
                ('duration_text_en', models.CharField(
                    blank=True, max_length=100, null=True,
                    help_text='مثلاً «حدود ۲ ساعت و ۳۰ دقیقه پرواز مستقیم»',
                    verbose_name='زمان تقریبی سفر',
                )),
                ('notes', models.TextField(
                    blank=True,
                    help_text='مثلاً نام شرکت‌های هواپیمایی، مرز مشترک، تعداد توقف و غیره.',
                    verbose_name='توضیحات اضافه',
                )),
                ('notes_fa', models.TextField(
                    blank=True, null=True,
                    help_text='مثلاً نام شرکت‌های هواپیمایی، مرز مشترک، تعداد توقف و غیره.',
                    verbose_name='توضیحات اضافه',
                )),
                ('notes_en', models.TextField(
                    blank=True, null=True,
                    help_text='مثلاً نام شرکت‌های هواپیمایی، مرز مشترک، تعداد توقف و غیره.',
                    verbose_name='توضیحات اضافه',
                )),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('destination_country', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='routes_to',
                    to='core.country',
                    verbose_name='کشور مقصد',
                )),
                ('origin_country', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='routes_from',
                    to='core.country',
                    verbose_name='کشور مبدا',
                )),
            ],
            options={
                'verbose_name': 'مسیر سفر',
                'verbose_name_plural': 'مسیرهای سفر',
                'ordering': ['destination_country', 'origin_country', 'mode'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='travelroute',
            unique_together={('origin_country', 'destination_country', 'mode')},
        ),
    ]
