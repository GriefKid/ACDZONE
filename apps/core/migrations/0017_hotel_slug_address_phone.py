from django.db import migrations, models
from django.utils.text import slugify


def backfill_slugs(apps, schema_editor):
    Hotel = apps.get_model('core', 'Hotel')
    for hotel in Hotel.objects.all():
        base = slugify(hotel.name_en or hotel.name_fa or hotel.name, allow_unicode=True) or 'hotel'
        slug = base
        n = 1
        while Hotel.objects.filter(country=hotel.country, slug=slug).exclude(pk=hotel.pk).exists():
            n += 1
            slug = f'{base}-{n}'
        hotel.slug = slug
        hotel.save(update_fields=['slug'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_expand_remaining_countries'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=180, verbose_name='نامک'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='address',
            field=models.CharField(blank=True, help_text='آدرس کامل هتل، توی صفحه‌ی جزئیات هتل نشان داده می‌شود.', max_length=255, verbose_name='آدرس'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='address_fa',
            field=models.CharField(blank=True, help_text='آدرس کامل هتل، توی صفحه‌ی جزئیات هتل نشان داده می‌شود.', max_length=255, null=True, verbose_name='آدرس'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='address_en',
            field=models.CharField(blank=True, help_text='آدرس کامل هتل، توی صفحه‌ی جزئیات هتل نشان داده می‌شود.', max_length=255, null=True, verbose_name='آدرس'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='phone_number',
            field=models.CharField(blank=True, help_text='مثلاً ‎+98 21 1234 5678', max_length=50, verbose_name='شماره تماس'),
        ),
        migrations.RunPython(backfill_slugs, noop),
        migrations.AlterUniqueTogether(
            name='hotel',
            unique_together={('country', 'slug')},
        ),
    ]
