from django.db import migrations
from django.utils.text import slugify

# A second real, well-known hotel for every country that only had one so
# far — doubles hotel coverage across the board per the user's explicit
# "بازم اولا کمه دیتاها" feedback. Contact details (address/phone) are left
# blank here rather than guessed; they can be filled in per-hotel from the
# admin as real front-desk info is gathered, and the hotel detail page
# already gracefully hides the address/phone block when empty.
SECOND_HOTELS = {
    'afghanistan': ('هتل اینترکانتیننتال کابل', 'Hotel Inter-Continental Kabul', 'کابل', 'Kabul', 4),
    'armenia': ('الکساندر لاکچری کالکشن ایروان', 'Alexander, a Luxury Collection Hotel, Yerevan', 'ایروان', 'Yerevan', 5),
    'azerbaijan': ('فرمونت باکو', 'Fairmont Baku, Flame Towers', 'باکو', 'Baku', 5),
    'bahrain': ('گالف هتل بحرین', 'The Gulf Hotel Bahrain', 'منامه', 'Manama', 5),
    'bangladesh': ('اینترکانتیننتال داکا', 'InterContinental Dhaka', 'داکا', 'Dhaka', 5),
    'bhutan': ('اوما پارو', 'Uma Paro (COMO Hotels)', 'پارو', 'Paro', 5),
    'brunei': ('ریزکون اینترنشنال هتل', 'Rizqun International Hotel', 'بندر سری‌بگاوان', 'Bandar Seri Begawan', 4),
    'cambodia': ('سوفیتل آنکور فوکیثرا', 'Sofitel Angkor Phokeethra Golf & Spa Resort', 'سیم‌ریپ', 'Siem Reap', 5),
    'china': ('پارک هایت پکن', 'Park Hyatt Beijing', 'پکن', 'Beijing', 5),
    'cyprus': ('آمارا هتل لیماسول', 'Amara Hotel Limassol', 'لیماسول', 'Limassol', 5),
    'georgia': ('رادیسون بلو ایوریا تفلیس', 'Radisson Blu Iveria Hotel, Tbilisi', 'تفلیس', 'Tbilisi', 5),
    'indonesia': ('فور سیزنز ریزورت بالی جیمباران', 'Four Seasons Resort Bali at Jimbaran Bay', 'جیمباران، بالی', 'Jimbaran, Bali', 5),
    'iraq': ('بابل روتانا بغداد', 'Babylon Rotana Baghdad', 'بغداد', 'Baghdad', 5),
    'israel': ('والدورف آستوریا اورشلیم', 'Waldorf Astoria Jerusalem', 'اورشلیم', 'Jerusalem', 5),
    'jordan': ('موونپیک ریزورت پترا', 'Mövenpick Resort Petra', 'پترا', 'Petra', 5),
    'kazakhstan': ('ریتز-کارلتون آلماتی', 'The Ritz-Carlton, Almaty', 'آلماتی', 'Almaty', 5),
    'kuwait': ('جمیرا مسیله بیچ هتل', 'Jumeirah Messilah Beach Hotel', 'شهر کویت', 'Kuwait City', 5),
    'kyrgyzstan': ('اوریون هتل بیشکک', 'Orion Hotel Bishkek', 'بیشکک', 'Bishkek', 4),
    'laos': ('امانتاکا لوانگ‌پرابانگ', 'Amantaka, Luang Prabang', 'لوانگ‌پرابانگ', 'Luang Prabang', 5),
    'lebanon': ('لو گری بیروت', 'Le Gray Beirut', 'بیروت', 'Beirut', 5),
    'malaysia': ('شانگری-لا کوالالامپور', 'Shangri-La Hotel Kuala Lumpur', 'کوالالامپور', 'Kuala Lumpur', 5),
    'maldives': ('کنراد مالدیو رنگالی', 'Conrad Maldives Rangali Island', 'رنگالی', 'Rangali Island', 5),
    'mongolia': ('بلو اسکای هتل اولان‌باتور', 'Blue Sky Hotel & Tower', 'اولان‌باتور', 'Ulaanbaatar', 5),
    'myanmar': ('سوفیتل یانگون', 'Sofitel Yangon', 'یانگون', 'Yangon', 5),
    'nepal': ('هایت ریجنسی کاتماندو', 'Hyatt Regency Kathmandu', 'کاتماندو', 'Kathmandu', 5),
    'north-korea': ('هتل کوریو پیونگ‌یانگ', 'Koryo Hotel', 'پیونگ‌یانگ', 'Pyongyang', 4),
    'oman': ('چدی مسقط', 'The Chedi Muscat', 'مسقط', 'Muscat', 5),
    'pakistan': ('سرنا هتل اسلام‌آباد', 'Islamabad Serena Hotel', 'اسلام‌آباد', 'Islamabad', 5),
    'palestine': ('گرند پارک هتل رام‌الله', 'The Grand Park Hotel Ramallah', 'رام‌الله', 'Ramallah', 5),
    'philippines': ('شانگری-لا اتذفورت مانیل', 'Shangri-La at the Fort, Manila', 'مانیل', 'Manila', 5),
    'qatar': ('ماندارین اورینتال دوحه', 'Mandarin Oriental, Doha', 'دوحه', 'Doha', 5),
    'russia': ('فور سیزنز لاین پالاس سن‌پترزبورگ', 'Four Seasons Hotel Lion Palace St. Petersburg', 'سن‌پترزبورگ', 'Saint Petersburg', 5),
    'saudi-arabia': ('ریتز-کارلتون ریاض', 'The Ritz-Carlton, Riyadh', 'ریاض', 'Riyadh', 5),
    'singapore': ('فولرتون هتل سنگاپور', 'The Fullerton Hotel Singapore', 'سنگاپور', 'Singapore', 5),
    'south-korea': ('شیلا هتل سئول', 'The Shilla Seoul', 'سئول', 'Seoul', 5),
    'sri-lanka': ('سینامون گرند کلمبو', 'Cinnamon Grand Colombo', 'کلمبو', 'Colombo', 5),
    'syria': ('شرایتون دمشق', 'Sheraton Damascus Hotel', 'دمشق', 'Damascus', 5),
    'taiwan': ('ماندارین اورینتال تایپه', 'Mandarin Oriental, Taipei', 'تایپه', 'Taipei', 5),
    'tajikistan': ('سرنا هتل دوشنبه', 'Serena Hotel Dushanbe', 'دوشنبه', 'Dushanbe', 4),
    'thailand': ('آناتارا سیام بانکوک', 'Anantara Siam Bangkok Hotel', 'بانکوک', 'Bangkok', 5),
    'timor-leste': ('نووو توریسمو هتل دیلی', 'Novo Turismo Hotel', 'دیلی', 'Dili', 3),
    'turkmenistan': ('هتل ییلدیز عشق‌آباد', 'Yyldyz Hotel', 'عشق‌آباد', 'Ashgabat', 4),
    'uzbekistan': ('هایت ریجنسی تاشکند', 'Hyatt Regency Tashkent', 'تاشکند', 'Tashkent', 5),
    'vietnam': ('اینترکانتیننتال دانانگ سان پنینسولا', 'InterContinental Danang Sun Peninsula Resort', 'دانانگ', 'Da Nang', 5),
    'yemen': ('شرایتون صنعا', "Sheraton Sana'a Hotel", 'صنعا', "Sana'a", 4),
}


def seed(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    Hotel = apps.get_model('core', 'Hotel')
    for slug, (name_fa, name_en, city_fa, city_en, stars) in SECOND_HOTELS.items():
        country = Country.objects.filter(slug=slug).first()
        if not country:
            continue
        if Hotel.objects.filter(country=country, name_en=name_en).exists():
            continue
        summary_fa = f'دومین هتل شناخته‌شده‌ی معرفی‌شده برای {country.name_fa or country.name}.'
        summary_en = f'A second well-known hotel featured for {country.name_en or name_en}.'
        base_slug = slugify(name_en, allow_unicode=True) or 'hotel'
        slug_val = base_slug
        n = 1
        while Hotel.objects.filter(country=country, slug=slug_val).exists():
            n += 1
            slug_val = f'{base_slug}-{n}'
        Hotel.objects.create(
            country=country,
            name=name_fa, name_fa=name_fa, name_en=name_en,
            slug=slug_val,
            city=city_fa, city_fa=city_fa, city_en=city_en,
            star_rating=stars,
            summary=summary_fa, summary_fa=summary_fa, summary_en=summary_en,
            description=summary_fa, description_fa=summary_fa, description_en=summary_en,
            image_url='',
            is_active=True, order=1,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_hotel_slug_address_phone_auto'),
    ]

    operations = [
        migrations.RunPython(seed, noop),
    ]
