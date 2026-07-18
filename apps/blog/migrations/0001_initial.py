import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel', models.CharField(choices=[('news', 'ACDNews'), ('notes', 'ACDNotes')], default='news', max_length=10)),
                ('category', models.CharField(
                    blank=True,
                    choices=[('sports', 'ورزشی'), ('economy', 'اقتصادی'), ('politics', 'سیاسی'), ('society', 'اجتماعی')],
                    help_text='فقط برای ACDNews. اگر خالی بماند و یکی از این چهار کلمه در تگ‌ها باشد، خودکار تشخیص داده می‌شود.',
                    max_length=20,
                )),
                ('title', models.CharField(max_length=220)),
                ('title_fa', models.CharField(max_length=220, null=True)),
                ('title_en', models.CharField(max_length=220, null=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=250, unique=True)),
                ('summary', models.TextField(blank=True, help_text='اگر خالی بماند، از ابتدای متن ساخته می‌شود.')),
                ('summary_fa', models.TextField(blank=True, help_text='اگر خالی بماند، از ابتدای متن ساخته می‌شود.', null=True)),
                ('summary_en', models.TextField(blank=True, help_text='اگر خالی بماند، از ابتدای متن ساخته می‌شود.', null=True)),
                ('body', models.TextField()),
                ('body_fa', models.TextField(null=True)),
                ('body_en', models.TextField(null=True)),
                ('tags', models.CharField(
                    blank=True,
                    help_text='با کاما جدا کنید. کلمات ورزشی/اقتصادی/سیاسی/اجتماعی خودکار از این لیست حذف و به دسته تبدیل می‌شوند.',
                    max_length=300,
                )),
                ('source_name', models.CharField(blank=True, help_text='فقط برای ACDNews', max_length=120)),
                ('source_url', models.URLField(blank=True, help_text='فقط برای ACDNews')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/')),
                ('image_url', models.URLField(blank=True, help_text='لینک عکس خارجی (اگر عکسی آپلود نشود، از همین لینک استفاده می‌شود)')),
                ('is_active', models.BooleanField(default=True)),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-published_at'],
            },
        ),
    ]
