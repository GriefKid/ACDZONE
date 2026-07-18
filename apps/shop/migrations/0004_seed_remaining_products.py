from django.db import migrations

VISACARD_SHORT_FA = 'کارت شارژ بین‌المللی ویزا، پذیرفته‌شده در اکثر فروشگاه‌های آنلاین دنیا.'
AB_SARD_SHORT_FA = 'تجربه‌ی پرواز با بالن بر فراز منطقه‌ی آب‌سرد.'
AHMADABAD_SHORT_FA = 'تجربه‌ی پرواز با بالن بر فراز احمدآباد مستوفی.'

# Real stock photography (Unsplash License — free for commercial use, no
# attribution required), not another hand-drawn graphic: a card graphic
# was tried once already and didn't look right, so this reverts to real
# photos. These are swappable in seconds from /admin/ — open the product,
# upload a real photo under "image" (it takes priority over image_url), no
# code change needed.
UNIONCARD_IMAGE = 'https://images.unsplash.com/photo-1556742031-c6961e8560b0?auto=format&fit=crop&w=1200&q=80'
VISACARD_IMAGE = 'https://images.unsplash.com/photo-1609429019995-8c40f49535a5?auto=format&fit=crop&w=1200&q=80'
AB_SARD_IMAGE = 'https://images.unsplash.com/photo-1758558364489-e6b0a03d1fcf?auto=format&fit=crop&w=1200&q=80'
AHMADABAD_IMAGE = 'https://images.unsplash.com/photo-1761828122700-11b752d69a88?auto=format&fit=crop&w=1200&q=80'


def seed_remaining_products(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Product = apps.get_model('shop', 'Product')

    # UnionCard: drop the hand-drawn SVG graphic in favour of a real photo.
    try:
        unioncard = Product.objects.get(title_fa='یونیون‌کارت')
        unioncard.image = ''
        unioncard.image_url = UNIONCARD_IMAGE
        unioncard.save(update_fields=['image', 'image_url'])
        cards_category = unioncard.category
    except Product.DoesNotExist:
        cards_category, _ = Category.objects.get_or_create(
            page='acdpay',
            name_fa='کارت‌های شارژ بین‌المللی',
            defaults={'name': 'کارت‌های شارژ بین‌المللی', 'order': 0, 'is_active': True},
        )

    Product.objects.get_or_create(
        category=cards_category,
        title_fa='ویزاکارت',
        defaults={
            'title': 'ویزاکارت',
            'description': VISACARD_SHORT_FA,
            'description_fa': VISACARD_SHORT_FA,
            'image_url': VISACARD_IMAGE,
            'price': 0,
            'is_active': True,
            'order': 1,
        },
    )

    balloons_category, _ = Category.objects.get_or_create(
        page='acdballoons',
        name_fa='بلیط بالن‌سواری',
        defaults={'name': 'بلیط بالن‌سواری', 'order': 0, 'is_active': True},
    )

    Product.objects.get_or_create(
        category=balloons_category,
        title_fa='بالن‌سواری آب‌سرد',
        defaults={
            'title': 'بالن‌سواری آب‌سرد',
            'description': AB_SARD_SHORT_FA,
            'description_fa': AB_SARD_SHORT_FA,
            'image_url': AB_SARD_IMAGE,
            'price': 0,
            'is_active': True,
            'order': 0,
        },
    )

    Product.objects.get_or_create(
        category=balloons_category,
        title_fa='بالن‌سواری احمدآباد مستوفی',
        defaults={
            'title': 'بالن‌سواری احمدآباد مستوفی',
            'description': AHMADABAD_SHORT_FA,
            'description_fa': AHMADABAD_SHORT_FA,
            'image_url': AHMADABAD_IMAGE,
            'price': 0,
            'is_active': True,
            'order': 1,
        },
    )


def remove_remaining_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Product.objects.filter(
        title_fa__in=['ویزاکارت', 'بالن‌سواری آب‌سرد', 'بالن‌سواری احمدآباد مستوفی'],
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_seed_unioncard'),
    ]

    operations = [
        migrations.RunPython(seed_remaining_products, remove_remaining_products),
    ]
