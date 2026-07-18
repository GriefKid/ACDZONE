from django.db import migrations

# Approximate flight distances/durations FROM Iran and the UAE (the
# project's two hub countries) TO every remaining country that had zero
# TravelRoute rows — this is why the calculator on pages like Bahrain's
# said "no info" no matter what was picked. Figures are well-known
# approximate great-circle air distances between capitals/major hubs,
# same approach and honesty-labeling as migration 0015.
ROUTES = [
    # (origin_slug, destination_slug, distance_km, duration_text)
    ('iran', 'armenia', 850, 'حدود ۱ ساعت و ۴۵ دقیقه پرواز مستقیم'),
    ('iran', 'azerbaijan', 650, 'حدود ۱ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('iran', 'bahrain', 1000, 'حدود ۱ ساعت و ۴۵ دقیقه پرواز مستقیم'),
    ('iran', 'bangladesh', 4200, 'حدود ۵ ساعت پرواز (معمولاً با یک توقف)'),
    ('iran', 'bhutan', 4800, 'حدود ۶ ساعت پرواز (معمولاً با یک توقف)'),
    ('iran', 'brunei', 7300, 'حدود ۹ ساعت پرواز (معمولاً با یک توقف)'),
    ('iran', 'cambodia', 6300, 'حدود ۷ ساعت و ۳۰ دقیقه پرواز (معمولاً با یک توقف)'),
    ('iran', 'cyprus', 2000, 'حدود ۳ ساعت پرواز مستقیم'),
    ('iran', 'georgia', 950, 'حدود ۲ ساعت پرواز مستقیم'),
    ('iran', 'iraq', 900, 'حدود ۱ ساعت و ۴۵ دقیقه پرواز مستقیم'),
    ('iran', 'israel', 1900, 'حدود ۳ ساعت پرواز (پرواز مستقیم معمولاً وجود ندارد)'),
    ('iran', 'kazakhstan', 2500, 'حدود ۳ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('iran', 'kuwait', 1200, 'حدود ۲ ساعت پرواز مستقیم'),
    ('iran', 'kyrgyzstan', 2800, 'حدود ۴ ساعت پرواز (معمولاً با یک توقف)'),
    ('iran', 'laos', 6100, 'حدود ۷ ساعت پرواز (معمولاً با یک توقف)'),
    ('iran', 'lebanon', 1900, 'حدود ۳ ساعت پرواز مستقیم'),
    ('iran', 'maldives', 3200, 'حدود ۴ ساعت و ۳۰ دقیقه پرواز (معمولاً با یک توقف)'),
    ('iran', 'mongolia', 4900, 'حدود ۶ ساعت پرواز (معمولاً با یک توقف)'),
    ('iran', 'myanmar', 5000, 'حدود ۶ ساعت پرواز (معمولاً با یک توقف)'),
    ('iran', 'nepal', 3600, 'حدود ۴ ساعت و ۳۰ دقیقه پرواز (معمولاً با یک توقف)'),
    ('iran', 'north-korea', 6600, 'حدود ۸ ساعت پرواز (معمولاً با یک یا دو توقف)'),
    ('iran', 'oman', 1300, 'حدود ۲ ساعت پرواز مستقیم'),
    ('iran', 'palestine', 1900, 'حدود ۳ ساعت پرواز (پرواز مستقیم معمولاً وجود ندارد)'),
    ('iran', 'philippines', 6900, 'حدود ۸ ساعت و ۳۰ دقیقه پرواز (معمولاً با یک توقف)'),
    ('iran', 'russia', 2500, 'حدود ۴ ساعت پرواز مستقیم'),
    ('iran', 'singapore', 6500, 'حدود ۷ ساعت و ۳۰ دقیقه پرواز (معمولاً با یک توقف)'),
    ('iran', 'sri-lanka', 4200, 'حدود ۵ ساعت پرواز (معمولاً با یک توقف)'),
    ('iran', 'syria', 1500, 'حدود ۲ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('iran', 'taiwan', 7100, 'حدود ۹ ساعت پرواز (معمولاً با یک توقف)'),
    ('iran', 'tajikistan', 1900, 'حدود ۲ ساعت و ۴۵ دقیقه پرواز مستقیم'),
    ('iran', 'timor-leste', 9000, 'حدود ۱۱ ساعت پرواز (معمولاً با یک یا دو توقف)'),
    ('iran', 'turkmenistan', 900, 'حدود ۱ ساعت و ۴۵ دقیقه پرواز مستقیم'),
    ('iran', 'uzbekistan', 1900, 'حدود ۲ ساعت و ۴۵ دقیقه پرواز مستقیم'),
    ('iran', 'yemen', 2100, 'حدود ۳ ساعت پرواز (معمولاً با یک توقف)'),

    ('united-arab-emirates', 'armenia', 2000, 'حدود ۳ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'azerbaijan', 1900, 'حدود ۲ ساعت و ۴۵ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'bahrain', 480, 'حدود ۱ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'bangladesh', 3300, 'حدود ۴ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'bhutan', 3900, 'حدود ۵ ساعت پرواز (معمولاً با یک توقف)'),
    ('united-arab-emirates', 'brunei', 6400, 'حدود ۷ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'cambodia', 5300, 'حدود ۶ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'cyprus', 2900, 'حدود ۴ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'georgia', 2000, 'حدود ۳ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'iraq', 1200, 'حدود ۲ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'israel', 2400, 'حدود ۳ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'kazakhstan', 3000, 'حدود ۴ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'kuwait', 830, 'حدود ۱ ساعت و ۲۰ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'kyrgyzstan', 2900, 'حدود ۴ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'laos', 5100, 'حدود ۶ ساعت پرواز (معمولاً با یک توقف)'),
    ('united-arab-emirates', 'lebanon', 2400, 'حدود ۳ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'maldives', 2800, 'حدود ۴ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'mongolia', 5000, 'حدود ۶ ساعت پرواز (معمولاً با یک توقف)'),
    ('united-arab-emirates', 'myanmar', 4100, 'حدود ۵ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'nepal', 2700, 'حدود ۳ ساعت و ۴۵ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'north-korea', 6700, 'حدود ۸ ساعت پرواز (معمولاً با یک یا دو توقف)'),
    ('united-arab-emirates', 'oman', 380, 'حدود ۱ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'palestine', 2400, 'حدود ۳ ساعت و ۳۰ دقیقه پرواز (معمولاً با یک توقف)'),
    ('united-arab-emirates', 'philippines', 6000, 'حدود ۸ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'russia', 4300, 'حدود ۵ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'singapore', 5800, 'حدود ۷ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'sri-lanka', 3300, 'حدود ۴ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'syria', 2000, 'حدود ۳ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'taiwan', 6200, 'حدود ۸ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'tajikistan', 2200, 'حدود ۳ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'timor-leste', 8100, 'حدود ۱۰ ساعت پرواز (معمولاً با یک توقف)'),
    ('united-arab-emirates', 'turkmenistan', 1500, 'حدود ۲ ساعت و ۱۵ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'uzbekistan', 2100, 'حدود ۳ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'yemen', 1600, 'حدود ۲ ساعت و ۱۵ دقیقه پرواز مستقیم'),
]

ROUTE_NOTE_FA = 'فاصله و زمان تقریبی پرواز مستقیم/معمول؛ ممکن است بسته به مسیر و ایرلاین متفاوت باشد.'
ROUTE_NOTE_EN = 'Approximate distance and typical flight duration; may vary by route and airline.'


def seed(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    TravelRoute = apps.get_model('core', 'TravelRoute')
    for origin_slug, dest_slug, distance_km, duration_text in ROUTES:
        origin = Country.objects.filter(slug=origin_slug).first()
        dest = Country.objects.filter(slug=dest_slug).first()
        if not origin or not dest:
            continue
        if TravelRoute.objects.filter(origin_country=origin, destination_country=dest, mode='air').exists():
            continue
        TravelRoute.objects.create(
            origin_country=origin, destination_country=dest, mode='air',
            distance_km=distance_km, duration_text=duration_text,
            notes=ROUTE_NOTE_FA, notes_fa=ROUTE_NOTE_FA, notes_en=ROUTE_NOTE_EN,
            is_active=True,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_hotel_price_estimates'),
    ]

    operations = [
        migrations.RunPython(seed, noop),
    ]
