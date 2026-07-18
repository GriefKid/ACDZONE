from django.db import migrations

# Demonstration seed for the new "هتل‌های معروف" section: 2-3 real,
# well-known hotels for each of the 8 countries already covered by
# 0007/0008 (Iran, Afghanistan, Turkey, Japan, Pakistan, UAE, Saudi
# Arabia, India). booking_url is deliberately left blank — pointing it at
# a real booking page needs verification this pass didn't have time for;
# the admin can add a real link per hotel from /admin/ later.

HOTELS = {
    'iran': [
        {
            'name_fa': 'هتل عباسی اصفهان', 'name_en': 'Abbasi Hotel, Isfahan',
            'city_fa': 'اصفهان', 'city_en': 'Isfahan', 'star_rating': 5,
            'summary_fa': 'کاروانسرای صفوی تبدیل‌شده به هتل، با حیاطی باغی در قلب اصفهان.',
            'summary_en': 'A former Safavid-era caravanserai converted into a hotel, with a garden courtyard in the heart of Isfahan.',
            'description_fa': 'هتل عباسی یکی از قدیمی‌ترین و زیباترین هتل‌های ایران است که در ساختمانی تاریخی از دوران صفویه با تزئینات کاشی‌کاری سنتی قرار دارد.',
            'description_en': 'One of Iran\'s oldest and most beautiful hotels, housed in a historic Safavid-era building with traditional tilework decoration.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/8/85/Abbasi_Hotel_Isfahan.jpg',
        },
        {
            'name_fa': 'هتل اسپیناس پالاس تهران', 'name_en': 'Espinas Palace Hotel, Tehran',
            'city_fa': 'تهران', 'city_en': 'Tehran', 'star_rating': 5,
            'summary_fa': 'یکی از مدرن‌ترین و مجهزترین هتل‌های پنج‌ستاره‌ی تهران.',
            'summary_en': 'One of Tehran\'s most modern and well-equipped five-star hotels.',
            'description_fa': 'هتل اسپیناس پالاس با امکانات رفاهی گسترده و طراحی مدرن، میزبان بسیاری از مسافران تجاری و گردشگران در تهران است.',
            'description_en': 'With extensive amenities and modern design, Espinas Palace hosts many business travelers and tourists in Tehran.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2e/Espinas_Palace_Hotel.jpg',
        },
    ],
    'afghanistan': [
        {
            'name_fa': 'هتل سرینا کابل', 'name_en': 'Kabul Serena Hotel',
            'city_fa': 'کابل', 'city_en': 'Kabul', 'star_rating': 5,
            'summary_fa': 'شناخته‌شده‌ترین هتل بین‌المللی افغانستان با استانداردهای بالای امنیتی و رفاهی.',
            'summary_en': 'Afghanistan\'s best-known international hotel, with high security and hospitality standards.',
            'description_fa': 'هتل سرینا کابل بخشی از زنجیره‌ی هتل‌های آقاخان است و میزبان دیپلمات‌ها، مقامات و مسافران تجاری بین‌المللی در کابل بوده است.',
            'description_en': 'Part of the Aga Khan-affiliated Serena hotel chain, it has hosted diplomats, officials, and international business travelers in Kabul.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/5/5a/Kabul_Serena_Hotel.jpg',
        },
    ],
    'turkey': [
        {
            'name_fa': 'هتل چیراغان پالاس کمپینسکی استانبول', 'name_en': 'Çırağan Palace Kempinski, Istanbul',
            'city_fa': 'استانبول', 'city_en': 'Istanbul', 'star_rating': 5,
            'summary_fa': 'کاخ عثمانی سابق بر ساحل بسفر، امروز یکی از لوکس‌ترین هتل‌های جهان.',
            'summary_en': 'A former Ottoman palace on the Bosphorus, today one of the most luxurious hotels in the world.',
            'description_fa': 'این هتل در کاخی تاریخی از دوران عثمانی با چشم‌اندازی مستقیم به تنگه بسفر قرار دارد و ترکیبی از تجمل مدرن و معماری کلاسیک را ارائه می‌دهد.',
            'description_en': 'Housed in a historic Ottoman-era palace with direct views of the Bosphorus, it blends modern luxury with classical architecture.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/8/8a/Ciragan_Palace_Kempinski.jpg',
        },
        {
            'name_fa': 'موزیوم هتل کاپادوکیا', 'name_en': 'Museum Hotel, Cappadocia',
            'city_fa': 'اوچ‌حصار، کاپادوکیا', 'city_en': 'Uçhisar, Cappadocia', 'star_rating': 5,
            'summary_fa': 'هتلی غارمانند لوکس با اتاق‌های تراشیده‌شده در سنگ، مشرف به دره‌های کاپادوکیا.',
            'summary_en': 'A luxury cave-style hotel with rooms carved into rock, overlooking the valleys of Cappadocia.',
            'description_fa': 'این هتل بوتیک با معماری غارمانند سنتی منطقه، تجربه‌ای منحصربه‌فرد از اقامت در دل صخره‌های کاپادوکیا ارائه می‌دهد.',
            'description_en': 'A boutique hotel with the region\'s traditional cave-style architecture, offering a unique stay carved into the rocks of Cappadocia.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/1/16/Museum_Hotel_Cappadocia.jpg',
        },
    ],
    'japan': [
        {
            'name_fa': 'هتل ریتز-کارلتون توکیو', 'name_en': 'The Ritz-Carlton, Tokyo',
            'city_fa': 'توکیو', 'city_en': 'Tokyo', 'star_rating': 5,
            'summary_fa': 'هتلی لوکس در طبقات بالای برج میدتاون توکیو با چشم‌اندازی از کوه فوجی در روزهای صاف.',
            'summary_en': 'A luxury hotel on the upper floors of Tokyo Midtown Tower, with views of Mount Fuji on clear days.',
            'description_fa': 'این هتل با اتاق‌های وسیع، اسپا و رستوران‌های ژاپنی و بین‌المللی، یکی از برترین هتل‌های پنج‌ستاره‌ی توکیو به‌شمار می‌رود.',
            'description_en': 'With spacious rooms, a spa, and Japanese and international restaurants, it ranks among Tokyo\'s top five-star hotels.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6f/Ritz_Carlton_Tokyo.jpg',
        },
        {
            'name_fa': 'گیون هاتاناکا (ریوکان سنتی کیوتو)', 'name_en': 'Gion Hatanaka, Kyoto',
            'city_fa': 'کیوتو', 'city_en': 'Kyoto', 'star_rating': 4,
            'summary_fa': 'اقامتگاه سنتی ژاپنی (ریوکان) در محله‌ی تاریخی گیون کیوتو.',
            'summary_en': 'A traditional Japanese inn (ryokan) in Kyoto\'s historic Gion district.',
            'description_fa': 'این ریوکان تجربه‌ی اصیل اقامت ژاپنی را با اتاق‌های تاتامی، چشمه‌ی آب‌گرم و پذیرایی سنتی کایسه‌کی ارائه می‌دهد.',
            'description_en': 'This ryokan offers an authentic Japanese stay with tatami rooms, an onsen bath, and traditional kaiseki dining.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/44/Gion_Kyoto_Street.jpg',
        },
    ],
    'pakistan': [
        {
            'name_fa': 'پرل کانتیننتال لاهور', 'name_en': 'Pearl Continental Hotel, Lahore',
            'city_fa': 'لاهور', 'city_en': 'Lahore', 'star_rating': 5,
            'summary_fa': 'یکی از شناخته‌شده‌ترین زنجیره‌های هتل لوکس پاکستان.',
            'summary_en': 'One of Pakistan\'s best-known luxury hotel chains.',
            'description_fa': 'پرل کانتیننتال لاهور با امکانات مدرن و موقعیت مرکزی، مقصدی محبوب برای مسافران تجاری و گردشگران در لاهور است.',
            'description_en': 'With modern amenities and a central location, Pearl Continental Lahore is a popular destination for business travelers and tourists.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/3/3a/Pearl_Continental_Lahore.jpg',
        },
    ],
    'united-arab-emirates': [
        {
            'name_fa': 'برج العرب جمیرا', 'name_en': 'Burj Al Arab Jumeirah',
            'city_fa': 'دبی', 'city_en': 'Dubai', 'star_rating': 5,
            'summary_fa': 'نمادین‌ترین هتل جهان با طراحی بادبان‌مانند بر جزیره‌ای مصنوعی در دبی.',
            'summary_en': 'The world\'s most iconic sail-shaped hotel, on an artificial island in Dubai.',
            'description_fa': 'برج العرب یکی از معدود هتل‌های «هفت‌ستاره» جهان است که با تزئینات طلاکاری‌شده و سوئیت‌های چندطبقه، تجملی بی‌نظیر ارائه می‌دهد.',
            'description_en': 'One of the world\'s few self-styled "seven-star" hotels, offering unmatched luxury with gold-leaf decor and multi-storey suites.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/9a/Burj_Al_Arab.jpg',
        },
        {
            'name_fa': 'اطلانتیس د پالم دبی', 'name_en': 'Atlantis, The Palm, Dubai',
            'city_fa': 'دبی', 'city_en': 'Dubai', 'star_rating': 5,
            'summary_fa': 'هتل رویایی در نوک جزیره‌ی نخل دبی، با پارک آبی و آکواریوم اختصاصی.',
            'summary_en': 'A resort at the tip of Palm Jumeirah island, with its own waterpark and aquarium.',
            'description_fa': 'اطلانتیس د پالم با معماری خیره‌کننده و جاذبه‌های تفریحی خانوادگی، یکی از پرطرفدارترین اقامتگاه‌های دبی است.',
            'description_en': 'With striking architecture and family-friendly attractions, Atlantis The Palm is one of Dubai\'s most popular resorts.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/8/85/Atlantis_The_Palm_Dubai.jpg',
        },
    ],
    'saudi-arabia': [
        {
            'name_fa': 'برج ساعت مکه فرمونت', 'name_en': 'Makkah Clock Royal Tower, Fairmont',
            'city_fa': 'مکه', 'city_en': 'Mecca', 'star_rating': 5,
            'summary_fa': 'یکی از بلندترین هتل‌های جهان، مشرف مستقیم به مسجدالحرام.',
            'summary_en': 'One of the tallest hotels in the world, directly overlooking the Masjid al-Haram.',
            'description_fa': 'این هتل بخشی از مجموعه‌ی برج ساعت مکه است و میزبان میلیون‌ها زائر در طول سال با دسترسی مستقیم به مسجدالحرام است.',
            'description_en': 'Part of the Abraj Al-Bait complex, this hotel hosts millions of pilgrims each year with direct access to the Masjid al-Haram.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/8/8e/Makkah_Clock_Royal_Tower.jpg',
        },
    ],
    'india': [
        {
            'name_fa': 'کاخ تاج محل بمبئی', 'name_en': 'The Taj Mahal Palace, Mumbai',
            'city_fa': 'بمبئی', 'city_en': 'Mumbai', 'star_rating': 5,
            'summary_fa': 'هتلی تاریخی و نمادین رو به دروازه‌ی هند در بمبئی.',
            'summary_en': 'A historic, iconic hotel facing the Gateway of India in Mumbai.',
            'description_fa': 'این هتل که در سال ۱۹۰۳ افتتاح شد، یکی از قدیمی‌ترین و مجلل‌ترین هتل‌های هند و نمادی از معماری دوران استعمار است.',
            'description_en': 'Opened in 1903, this is one of India\'s oldest and most luxurious hotels, and a symbol of colonial-era architecture.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6e/Taj_Mahal_Palace_Hotel_Mumbai.jpg',
        },
        {
            'name_fa': 'اوبروی اودایویلاس', 'name_en': 'The Oberoi Udaivilas',
            'city_fa': 'اودیپور', 'city_en': 'Udaipur', 'star_rating': 5,
            'summary_fa': 'اقامتگاهی به‌سبک کاخ‌های راجستانی بر ساحل دریاچه‌ی پیچولا.',
            'summary_en': 'A Rajasthani palace-style resort on the shores of Lake Pichola.',
            'description_fa': 'این هتل بارها به‌عنوان یکی از بهترین هتل‌های جهان معرفی شده و ترکیبی از معماری سنتی راجستانی و چشم‌اندازی رویایی به دریاچه ارائه می‌دهد.',
            'description_en': 'Repeatedly ranked among the world\'s best hotels, it combines traditional Rajasthani architecture with a dreamlike lake view.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6a/Oberoi_Udaivilas.jpg',
        },
    ],
}


def seed(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    Hotel = apps.get_model('core', 'Hotel')

    for slug, items in HOTELS.items():
        try:
            country = Country.objects.get(slug=slug)
        except Country.DoesNotExist:
            continue
        for order, data in enumerate(items):
            exists = Hotel.objects.filter(country=country, name_en=data['name_en']).exists()
            if exists:
                continue
            Hotel.objects.create(
                country=country,
                name=data['name_fa'],
                name_fa=data['name_fa'],
                name_en=data['name_en'],
                city=data['city_fa'],
                city_fa=data['city_fa'],
                city_en=data['city_en'],
                star_rating=data['star_rating'],
                summary=data['summary_fa'],
                summary_fa=data['summary_fa'],
                summary_en=data['summary_en'],
                description=data['description_fa'],
                description_fa=data['description_fa'],
                description_en=data['description_en'],
                image_url=data['image_url'],
                order=order,
            )


def unseed(apps, schema_editor):
    # No-op — same reasoning as the other seed migrations in this project.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_hotel'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
