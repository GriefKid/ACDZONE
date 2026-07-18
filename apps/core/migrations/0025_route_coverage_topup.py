# Fixes the route calculator only having ONE origin option (Iran) for a
# handful of destination countries — afghanistan, india, pakistan,
# saudi-arabia, united-arab-emirates — while every other country already
# had two (Iran + UAE, added in 0022). Same pattern: add
# united-arab-emirates as a second origin for those four, and add one more
# origin (turkey) for united-arab-emirates itself so every one of the 50
# country pages ends up with the same two-origin baseline.
from django.db import migrations

# (origin_slug, destination_slug, distance_km, duration_text_fa, duration_text_en)
ROUTES = [
    ('united-arab-emirates', 'afghanistan', 2500, 'حدود ۳ ساعت و ۱۵ دقیقه پرواز مستقیم', 'About 3h15m direct flight'),
    ('united-arab-emirates', 'india', 2200, 'حدود ۳ ساعت پرواز مستقیم', 'About 3 hours direct flight'),
    ('united-arab-emirates', 'pakistan', 1200, 'حدود ۲ ساعت پرواز مستقیم', 'About 2 hours direct flight'),
    ('united-arab-emirates', 'saudi-arabia', 900, 'حدود ۱ ساعت و ۴۵ دقیقه پرواز مستقیم', 'About 1h45m direct flight'),
    ('turkey', 'united-arab-emirates', 3000, 'حدود ۴ ساعت پرواز مستقیم', 'About 4 hours direct flight'),
]

ROUTE_NOTE_FA = 'فاصله و زمان تقریبی پرواز مستقیم/معمول؛ ممکن است بسته به مسیر و ایرلاین متفاوت باشد.'
ROUTE_NOTE_EN = 'Approximate distance and typical flight duration; may vary by route and airline.'


def seed(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    TravelRoute = apps.get_model('core', 'TravelRoute')
    for origin_slug, dest_slug, distance_km, duration_fa, duration_en in ROUTES:
        origin = Country.objects.filter(slug=origin_slug).first()
        dest = Country.objects.filter(slug=dest_slug).first()
        if not origin or not dest:
            continue
        if TravelRoute.objects.filter(origin_country=origin, destination_country=dest, mode='air').exists():
            continue
        TravelRoute.objects.create(
            origin_country=origin, destination_country=dest, mode='air',
            distance_km=distance_km,
            duration_text=duration_fa, duration_text_fa=duration_fa, duration_text_en=duration_en,
            notes=ROUTE_NOTE_FA, notes_fa=ROUTE_NOTE_FA, notes_en=ROUTE_NOTE_EN,
            is_active=True,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_seed_country_weather'),
    ]

    operations = [
        migrations.RunPython(seed, noop),
    ]
