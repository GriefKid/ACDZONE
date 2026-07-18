from django.db import migrations
from django.utils.text import slugify

# Attractions for 8 more countries, all images verified via WebSearch against
# real Wikimedia Commons filenames (Special:FilePath redirect — no hash-path
# guessing). Each entry: (name_fa, name_en, summary_fa, summary_en, commons_filename)
ATTRACTIONS = {
    'china': [
        ('دیوار بزرگ چین', 'The Great Wall of China',
         'یکی از عظیم‌ترین سازه‌های ساخت بشر که برای هزاران کیلومتر در شمال چین امتداد دارد.',
         'One of the greatest structures ever built by humankind, stretching for thousands of kilometers across northern China.',
         'Great Wall of China, Beijing (27780841820).jpg'),
        ('شهر ممنوعه', 'The Forbidden City',
         'کاخ سلطنتی امپراتوران چین در قلب پکن که امروز موزه‌ای عظیم است.',
         'The imperial palace of China\'s emperors in the heart of Beijing, today a vast museum.',
         'The Forbidden City, Beijing, China (故宫博物院).jpg'),
    ],
    'thailand': [
        ('کاخ بزرگ بانکوک', 'The Grand Palace, Bangkok',
         'مجموعه‌ای باشکوه از کاخ‌ها و معابد که زمانی محل سکونت پادشاهان تایلند بود.',
         'A magnificent complex of palaces and temples that once housed Thailand\'s kings.',
         'Grand Palace Bangkok.jpg'),
        ('معبد وات آرون', 'Wat Arun (Temple of Dawn)',
         'معبد بودایی معروف بر ساحل رودخانه‌ی چائوپرایا با برج مرکزی خیره‌کننده.',
         'A famous Buddhist temple on the bank of the Chao Phraya River, with a striking central spire.',
         'Wat Arun from Chao Phraya River at sunset.jpg'),
    ],
    'vietnam': [
        ('خلیج هالونگ', 'Ha Long Bay',
         'خلیجی با هزاران صخره‌ی آهکی برخاسته از دریای زمرد‌گون، ثبت‌شده در یونسکو.',
         'A bay with thousands of limestone karsts rising from emerald waters, a UNESCO World Heritage Site.',
         'Ha Long Bay.jpg'),
        ('شهر باستانی هوی‌آن', 'Hoi An Ancient Town',
         'بندری تاریخی با خانه‌های چوبی رنگارنگ و فانوس‌های سنتی، ثبت‌شده در یونسکو.',
         'A historic trading port with colorful wooden houses and traditional lanterns, a UNESCO World Heritage Site.',
         'Hoi An Ancient town.jpg'),
    ],
    'malaysia': [
        ('برج‌های دوقلوی پتروناس', 'Petronas Twin Towers',
         'زمانی بلندترین ساختمان‌های جهان و نماد معماری مدرن کوالالامپور.',
         'Once the tallest buildings in the world and a symbol of Kuala Lumpur\'s modern skyline.',
         'Petronas Towers view2, Kuala Lumpur.jpg'),
        ('غارهای باتو', 'Batu Caves',
         'مجموعه‌ای از غارهای آهکی و معابد هندو با مجسمه‌ی عظیم موروگان در ورودی.',
         'A complex of limestone caves and Hindu temples, with a giant statue of Murugan at the entrance.',
         'Kuala Lumpur Batu Caves 0001.jpg'),
    ],
    'indonesia': [
        ('معبد بوروبودور', 'Borobudur Temple',
         'بزرگ‌ترین معبد بودایی جهان، بنایی عظیم از قرن نهم میلادی در جاوه.',
         'The world\'s largest Buddhist temple, a monumental 9th-century structure in Java.',
         'Borobudur Temple.jpg'),
        ('معبد تاناه‌لوت', 'Tanah Lot Temple',
         'معبد هندو بر صخره‌ای در دل دریا در بالی، یکی از نمادی‌ترین مناظر این جزیره.',
         'A Hindu temple perched on a rock formation in the sea in Bali, one of the island\'s most iconic sights.',
         'Pura Tanah Lot.jpg'),
    ],
    'south-korea': [
        ('کاخ گیونگ‌بوک‌گونگ', 'Gyeongbokgung Palace',
         'بزرگ‌ترین و باشکوه‌ترین کاخ سلسله‌ی جوسان در سئول.',
         'The largest and grandest of the palaces built by the Joseon Dynasty in Seoul.',
         'Seoul Gyeongbokgung palace exterior view.jpg'),
        ('جزیره‌ی جیجو', 'Jeju Island',
         'جزیره‌ای آتشفشانی با چشم‌اندازهای طبیعی خیره‌کننده، ثبت‌شده در یونسکو.',
         'A volcanic island with stunning natural scenery, a UNESCO World Heritage Site.',
         'Jeju Island.jpg'),
    ],
    'jordan': [
        ('پترا', 'Petra (Al-Khazneh)',
         'شهر باستانی تراشیده‌شده در صخره‌های سرخ توسط تمدن نبطی، یکی از هفت عجایب جهان نو.',
         'The ancient city carved into red sandstone cliffs by the Nabataeans, one of the New Seven Wonders of the World.',
         'Al-Khazneh (The Treasury), Petra, Jordan.jpg'),
        ('صحرای وادی‌رم', 'Wadi Rum Desert',
         'صحرایی با چشم‌اندازهای مریخ‌گونه که مقصدی محبوب برای سافاری و طبیعت‌گردی است.',
         'A desert with Mars-like landscapes, a popular destination for desert safaris and nature tourism.',
         'Wadi Rum Protected Area, Jordan.jpg'),
    ],
    'qatar': [
        ('موزه‌ی هنر اسلامی', 'Museum of Islamic Art, Doha',
         'یکی از برجسته‌ترین موزه‌های هنر اسلامی جهان با معماری خیره‌کننده روی جزیره‌ای مصنوعی.',
         'One of the world\'s foremost museums of Islamic art, with striking architecture on an artificial island.',
         'Museum of Islamic Art, Doha - 54726299556.jpg'),
        ('بازار سوق واقف', 'Souq Waqif',
         'بازار سنتی و پرجنب‌وجوش دوحه با معماری قدیمی و مغازه‌های صنایع‌دستی.',
         'Doha\'s traditional, bustling market with old-style architecture and handicraft shops.',
         'Doha Souq Waqif 1.jpg'),
    ],
}

# Hotels for the same 8 countries. Only 3 have a confirmed specific-property
# Commons photo (Peninsula Beijing, Oriental Hotel Bangkok, Lotte Hotel
# Seoul); the rest are left without a photo rather than guessed, per the
# lesson learned earlier in this project.
HOTELS = {
    'china': [
        ('د پنینسولا بیجینگ', 'The Peninsula Beijing', 'پکن', 'Beijing', 5,
         'هتلی افسانه‌ای در نزدیکی شهر ممنوعه با میراثی طولانی از میهمان‌نوازی لوکس.',
         'A legendary hotel near the Forbidden City with a long heritage of luxury hospitality.',
         'The Peninsula Beijing in 2017.jpg'),
    ],
    'thailand': [
        ('ماندارین اورینتال بانکوک', 'Mandarin Oriental Bangkok', 'بانکوک', 'Bangkok', 5,
         'یکی از قدیمی‌ترین و مشهورترین هتل‌های لوکس آسیا بر ساحل رودخانه‌ی چائوپرایا.',
         'One of Asia\'s oldest and most celebrated luxury hotels, on the bank of the Chao Phraya River.',
         'Oriental Hotel Bangkok Lobby.JPG'),
    ],
    'vietnam': [
        ('سوفیتل لجند متروپل هانوی', 'Sofitel Legend Metropole Hanoi', 'هانوی', 'Hanoi', 5,
         'هتلی تاریخی با معماری استعماری فرانسوی در قلب هانوی.',
         'A historic hotel with French colonial architecture in the heart of Hanoi.',
         ''),
    ],
    'malaysia': [
        ('ماندارین اورینتال کوالالامپور', 'Mandarin Oriental Kuala Lumpur', 'کوالالامپور', 'Kuala Lumpur', 5,
         'هتلی لوکس با چشم‌اندازی مستقیم به برج‌های پتروناس.',
         'A luxury hotel with a direct view of the Petronas Twin Towers.',
         ''),
    ],
    'indonesia': [
        ('مولیا بالی', 'The Mulia Bali', 'نوسا دوآ، بالی', 'Nusa Dua, Bali', 5,
         'استراحتگاهی ساحلی لوکس در جنوب بالی با سواحل خصوصی.',
         'A luxury beachfront resort in southern Bali with private beaches.',
         ''),
    ],
    'south-korea': [
        ('هتل لوته سئول', 'Lotte Hotel Seoul', 'سئول', 'Seoul', 5,
         'یکی از برج‌های میهمان‌نوازی برجسته‌ی سئول در منطقه‌ی تجاری میونگ‌دونگ.',
         'One of Seoul\'s landmark hospitality towers, in the Myeongdong commercial district.',
         'Lotte Hotel Seoul.JPG'),
    ],
    'jordan': [
        ('کمپینسکی هتل عمان', 'Kempinski Hotel Amman', 'امان', 'Amman', 5,
         'هتلی لوکس در قلب امان با معماری مدرن و خدمات درجه‌یک.',
         'A luxury hotel in the heart of Amman with modern architecture and top-tier service.',
         ''),
    ],
    'qatar': [
        ('ریتز-کارلتون دوحه', 'The Ritz-Carlton, Doha', 'دوحه', 'Doha', 5,
         'استراحتگاهی ساحلی لوکس با ساحل خصوصی و مارینا در دوحه.',
         'A luxury beachfront resort with a private beach and marina in Doha.',
         ''),
    ],
}

# Approximate flight distances/durations FROM two of the project's original
# hub countries (Iran, United Arab Emirates) TO each of these 8 new
# countries. Figures are well-known approximate great-circle air distances
# between capitals/major hubs, deliberately labelled "approximate" in notes.
ROUTES = [
    # (origin_slug, destination_slug, mode, distance_km, duration_text)
    ('iran', 'china', 'air', 5900, 'حدود ۷ ساعت پرواز مستقیم'),
    ('iran', 'thailand', 'air', 5300, 'حدود ۶ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('iran', 'vietnam', 'air', 6350, 'حدود ۷ ساعت و ۳۰ دقیقه پرواز (معمولاً با یک توقف)'),
    ('iran', 'malaysia', 'air', 6300, 'حدود ۷ ساعت و ۳۰ دقیقه پرواز (معمولاً با یک توقف)'),
    ('iran', 'indonesia', 'air', 7300, 'حدود ۹ ساعت پرواز (معمولاً با یک توقف)'),
    ('iran', 'south-korea', 'air', 6700, 'حدود ۸ ساعت پرواز مستقیم'),
    ('iran', 'jordan', 'air', 1550, 'حدود ۲ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('iran', 'qatar', 'air', 1000, 'حدود ۱ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'china', 'air', 5980, 'حدود ۷ ساعت و ۱۵ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'thailand', 'air', 4880, 'حدود ۶ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'vietnam', 'air', 5730, 'حدود ۷ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'malaysia', 'air', 5920, 'حدود ۷ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'indonesia', 'air', 6800, 'حدود ۸ ساعت پرواز مستقیم (بالی: حدود ۹ ساعت)'),
    ('united-arab-emirates', 'south-korea', 'air', 6980, 'حدود ۸ ساعت و ۳۰ دقیقه پرواز مستقیم'),
    ('united-arab-emirates', 'jordan', 'air', 1930, 'حدود ۳ ساعت پرواز مستقیم'),
    ('united-arab-emirates', 'qatar', 'air', 380, 'حدود ۱ ساعت پرواز مستقیم'),
]

ROUTE_NOTE_FA = 'فاصله و زمان تقریبی پرواز مستقیم/معمول؛ ممکن است بسته به مسیر و ایرلاین متفاوت باشد.'
ROUTE_NOTE_EN = 'Approximate distance and typical direct-flight duration; may vary by route and airline.'


def commons_url(filename):
    from urllib.parse import quote
    return 'https://commons.wikimedia.org/wiki/Special:FilePath/' + quote(filename.replace(' ', '_'))


def seed(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    Attraction = apps.get_model('core', 'Attraction')
    Hotel = apps.get_model('core', 'Hotel')
    TravelRoute = apps.get_model('core', 'TravelRoute')

    for slug, items in ATTRACTIONS.items():
        country = Country.objects.filter(slug=slug).first()
        if not country:
            continue
        for order, (name_fa, name_en, summary_fa, summary_en, filename) in enumerate(items):
            if Attraction.objects.filter(country=country, name_en=name_en).exists():
                continue
            base_slug = slugify(name_en, allow_unicode=True) or 'attraction'
            slug = base_slug
            n = 1
            while Attraction.objects.filter(country=country, slug=slug).exists():
                n += 1
                slug = f'{base_slug}-{n}'
            Attraction.objects.create(
                country=country,
                name=name_fa, name_fa=name_fa, name_en=name_en,
                slug=slug,
                summary=summary_fa, summary_fa=summary_fa, summary_en=summary_en,
                description=summary_fa, description_fa=summary_fa, description_en=summary_en,
                image_url=commons_url(filename) if filename else '',
                is_active=True, order=order,
            )

    for slug, items in HOTELS.items():
        country = Country.objects.filter(slug=slug).first()
        if not country:
            continue
        for order, (name_fa, name_en, city_fa, city_en, stars, summary_fa, summary_en, filename) in enumerate(items):
            if Hotel.objects.filter(country=country, name_en=name_en).exists():
                continue
            Hotel.objects.create(
                country=country,
                name=name_fa, name_fa=name_fa, name_en=name_en,
                city=city_fa, city_fa=city_fa, city_en=city_en,
                star_rating=stars,
                summary=summary_fa, summary_fa=summary_fa, summary_en=summary_en,
                description=summary_fa, description_fa=summary_fa, description_en=summary_en,
                image_url=commons_url(filename) if filename else '',
                is_active=True, order=order,
            )

    for origin_slug, dest_slug, mode, distance_km, duration_text in ROUTES:
        origin = Country.objects.filter(slug=origin_slug).first()
        dest = Country.objects.filter(slug=dest_slug).first()
        if not origin or not dest:
            continue
        if TravelRoute.objects.filter(origin_country=origin, destination_country=dest, mode=mode).exists():
            continue
        TravelRoute.objects.create(
            origin_country=origin, destination_country=dest, mode=mode,
            distance_km=distance_km, duration_text=duration_text,
            notes=ROUTE_NOTE_FA, notes_fa=ROUTE_NOTE_FA, notes_en=ROUTE_NOTE_EN,
            is_active=True,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_all_countries_facts_and_descriptions'),
    ]

    operations = [
        migrations.RunPython(seed, noop),
    ]
