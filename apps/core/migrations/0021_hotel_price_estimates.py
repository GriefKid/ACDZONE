from django.db import migrations

# Approximate nightly price-per-star baseline (USD). This site has no real
# booking/rates API, so every value here is a deliberately-labeled ESTIMATE
# (see Hotel.price_usd help_text and the "قیمت تقریبی" wording on the hotel
# detail page) built from star rating × a rough relative cost-of-living
# multiplier per country — not a live quote. It exists so the price
# comparison charts (templates/core/hotel_detail.html) have real numbers to
# plot; swap in actual rates from the admin any time a real one is known.
BASE_PRICE_BY_STAR = {3: 60, 4: 100, 5: 180}

HIGH_COST = {
    'united-arab-emirates', 'qatar', 'saudi-arabia', 'kuwait', 'singapore',
    'japan', 'south-korea', 'israel', 'russia', 'maldives', 'bahrain',
    'brunei', 'taiwan', 'cyprus',
}
LOW_COST = {
    'iran', 'afghanistan', 'pakistan', 'india', 'bangladesh', 'nepal',
    'bhutan', 'myanmar', 'cambodia', 'laos', 'kyrgyzstan', 'tajikistan',
    'turkmenistan', 'yemen', 'syria', 'palestine', 'north-korea', 'timor-leste',
}
# Everything else (Turkey, China, Malaysia, Thailand, Jordan, Oman,
# Azerbaijan, Georgia, Armenia, Kazakhstan, Uzbekistan, Vietnam, Indonesia,
# Philippines, Sri Lanka, Lebanon, Iraq, Mongolia, ...) uses the mid tier.


def multiplier_for(slug):
    if slug in HIGH_COST:
        return 1.3
    if slug in LOW_COST:
        return 0.75
    return 1.0


def apply_estimates(apps, schema_editor):
    Hotel = apps.get_model('core', 'Hotel')
    for hotel in Hotel.objects.select_related('country').filter(price_usd__isnull=True):
        base = BASE_PRICE_BY_STAR.get(hotel.star_rating, 90)
        mult = multiplier_for(hotel.country.slug)
        price = round(base * mult / 5) * 5  # round to nearest $5
        hotel.price_usd = price
        hotel.save(update_fields=['price_usd'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_hotel_price_usd'),
    ]

    operations = [
        migrations.RunPython(apply_estimates, noop),
    ]
