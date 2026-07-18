import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوادگی')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=180, unique=True, verbose_name='نامک')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='representatives/photos/', verbose_name='عکس نماینده')),
                ('photo_url', models.URLField(blank=True, help_text='اگر عکس آپلود نشود، از این لینک استفاده می‌شود.', verbose_name='لینک عکس نماینده')),
                ('phone', models.CharField(blank=True, max_length=40, verbose_name='شماره تماس')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='ایمیل')),
                ('position', models.CharField(blank=True, max_length=120, verbose_name='عنوان')),
                ('bio', models.TextField(blank=True, verbose_name='توضیحات')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='ترتیب')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='representatives', to='core.country', verbose_name='کشور')),
            ],
            options={
                'verbose_name': 'نماینده',
                'verbose_name_plural': 'نماینده‌ها',
                'ordering': ['order', 'id'],
            },
        ),
    ]
