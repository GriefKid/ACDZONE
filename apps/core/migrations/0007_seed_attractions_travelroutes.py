from django.db import migrations


# Demonstration seed data — NOT full 36-country coverage. This shows the
# admin what real, filled-in Attraction/TravelRoute rows should look like
# for four countries (Iran, Turkey, Japan, Afghanistan): 2-3 real
# attractions each (real names/descriptions, Wikimedia Commons photo
# links) plus a handful of real travel routes between them. Every other
# country's accordions will show the "nothing added yet" empty state
# until an admin fills them in from /admin/ — the models/admin fully
# support that already, this migration just seeds a working example.
COUNTRIES = {
    'iran': {
        'name_fa': 'ایران', 'name_en': 'Iran',
        'description_fa': 'ایران، سرزمینی با هزاران سال تاریخ تمدن، از تخت جمشید تا میدان نقش جهان اصفهان، یکی از غنی‌ترین مقصدهای گردشگری خاورمیانه است.',
        'description_en': 'Iran, home to thousands of years of civilization, from Persepolis to Isfahan\'s Naqsh-e Jahan Square, is one of the richest tourist destinations in the Middle East.',
        'background_image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/28/Persepolis_24.11.2009_09-63.jpg',
    },
    'turkey': {
        'name_fa': 'ترکیه', 'name_en': 'Turkey',
        'description_fa': 'ترکیه با پیوند دو قاره‌ی آسیا و اروپا، میزبان جاذبه‌هایی چون ایاصوفیه و کاپادوکیا و سواحل زیبای مدیترانه است.',
        'description_en': 'Bridging Asia and Europe, Turkey hosts landmarks like the Hagia Sophia and Cappadocia, alongside its beautiful Mediterranean coastline.',
        'background_image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Cappadocia_Balloons.jpg',
    },
    'japan': {
        'name_fa': 'ژاپن', 'name_en': 'Japan',
        'description_fa': 'ژاپن، ترکیبی از سنت و تکنولوژی، از کوه فوجی گرفته تا معابد کیوتو، مقصدی رویایی برای گردشگران است.',
        'description_en': 'Japan blends tradition and technology — from Mount Fuji to the temples of Kyoto — into a dream destination for travelers.',
        'background_image_url': 'https://upload.wikimedia.org/wikipedia/commons/3/34/MtFuji_FromNagaokaFireworks_2004-8-1.jpg',
    },
    'afghanistan': {
        'name_fa': 'افغانستان', 'name_en': 'Afghanistan',
        'description_fa': 'افغانستان با طبیعتی خیره‌کننده مثل دریاچه‌های بند امیر و تاریخی کهن، مقصدی کمتر دیده‌شده اما شگفت‌انگیز است.',
        'description_en': 'With stunning nature like the Band-e-Amir lakes and an ancient history, Afghanistan is a lesser-seen but remarkable destination.',
        'background_image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2a/Band-e-Amir_National_Park.jpg',
    },
}

ATTRACTIONS = {
    'iran': [
        {
            'name_fa': 'تخت جمشید', 'name_en': 'Persepolis',
            'summary_fa': 'پایتخت تشریفاتی امپراتوری هخامنشی، یکی از باشکوه‌ترین بناهای باستانی جهان.',
            'summary_en': 'The ceremonial capital of the Achaemenid Empire, one of the world\'s grandest ancient sites.',
            'description_fa': 'تخت جمشید در نزدیکی شیراز، به دستور داریوش بزرگ بنا شد و نمادی از قدرت و هنر معماری امپراتوری هخامنشی است. این مجموعه در فهرست میراث جهانی یونسکو ثبت شده و هرساله گردشگران زیادی را از سراسر جهان به خود جذب می‌کند.',
            'description_en': 'Built near Shiraz on the order of Darius the Great, Persepolis symbolizes the power and architectural artistry of the Achaemenid Empire. A UNESCO World Heritage Site, it draws visitors from around the world every year.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/28/Persepolis_24.11.2009_09-63.jpg',
        },
        {
            'name_fa': 'میدان نقش جهان اصفهان', 'name_en': 'Naqsh-e Jahan Square, Isfahan',
            'summary_fa': 'یکی از بزرگ‌ترین میدان‌های تاریخی جهان، محاطه‌شده با مساجد و کاخ‌های صفوی.',
            'summary_en': 'One of the largest historic squares in the world, ringed by Safavid-era mosques and palaces.',
            'description_fa': 'میدان نقش جهان در قلب اصفهان، شاهکاری از معماری دوره‌ی صفوی است که مسجد شاه، مسجد شیخ لطف‌الله، کاخ عالی‌قاپو و بازار سنتی قیصریه را در خود جای داده است.',
            'description_en': 'At the heart of Isfahan, Naqsh-e Jahan Square is a Safavid-era masterpiece housing the Shah Mosque, Sheikh Lotfollah Mosque, Ali Qapu Palace, and the historic Qeysarieh bazaar.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/9d/Naghsh-e_Jahan_Square%2C_Isfahan%2C_Iran.jpg',
        },
    ],
    'turkey': [
        {
            'name_fa': 'ایاصوفیه', 'name_en': 'Hagia Sophia',
            'summary_fa': 'بنایی تاریخی در استانبول که در طول تاریخ کلیسا، مسجد و موزه بوده است.',
            'summary_en': 'A historic Istanbul landmark that has served as a church, mosque, and museum throughout history.',
            'description_fa': 'ایاصوفیه با گنبد عظیم و موزاییک‌های بی‌نظیرش، نمادی از تلاقی تمدن‌های روم شرقی و عثمانی است و یکی از پربازدیدترین بناهای استانبول به‌شمار می‌رود.',
            'description_en': 'With its immense dome and remarkable mosaics, Hagia Sophia symbolizes the meeting of Byzantine and Ottoman civilizations and remains one of Istanbul\'s most visited landmarks.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/a/a4/Hagia_Sophia_Mars_2013.jpg',
        },
        {
            'name_fa': 'کاپادوکیا', 'name_en': 'Cappadocia',
            'summary_fa': 'منطقه‌ای با ستون‌های صخره‌ای شگفت‌انگیز و پرواز بالن‌های هوای گرم.',
            'summary_en': 'A region of surreal rock formations, famous for its hot air balloon flights.',
            'description_fa': 'کاپادوکیا با دودکش‌های پریان، شهرهای زیرزمینی و پرواز صبحگاهی بالن‌های هوای گرم، یکی از خاص‌ترین چشم‌اندازهای طبیعی ترکیه است.',
            'description_en': 'With its fairy chimneys, underground cities, and sunrise hot air balloon rides, Cappadocia offers one of Turkey\'s most unique landscapes.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Cappadocia_Balloons.jpg',
        },
    ],
    'japan': [
        {
            'name_fa': 'کوه فوجی', 'name_en': 'Mount Fuji',
            'summary_fa': 'بلندترین قله ژاپن و نمادی ملی و معنوی برای مردم این کشور.',
            'summary_en': 'Japan\'s tallest peak and a national and spiritual symbol for its people.',
            'description_fa': 'کوه فوجی با قله‌ی مخروطی متقارن و پوشیده از برف، در فهرست میراث جهانی یونسکو ثبت شده و مقصدی محبوب برای کوه‌نوردی و عکاسی است.',
            'description_en': 'With its symmetrical, snow-capped cone, Mount Fuji is a UNESCO World Heritage Site and a popular destination for hiking and photography.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/3/34/MtFuji_FromNagaokaFireworks_2004-8-1.jpg',
        },
        {
            'name_fa': 'معبد فوشیمی ایناری', 'name_en': 'Fushimi Inari Shrine',
            'summary_fa': 'معبدی در کیوتو، مشهور به هزاران دروازه‌ی توری نارنجی‌رنگ.',
            'summary_en': 'A Kyoto shrine famous for its thousands of vermillion torii gates.',
            'description_fa': 'فوشیمی ایناری با مسیر پیاده‌روی میان هزاران دروازه‌ی توری، یکی از نمادی‌ترین جاذبه‌های کیوتو و ژاپن است.',
            'description_en': 'With its walking trail through thousands of torii gates, Fushimi Inari is one of the most iconic sights in Kyoto and Japan.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/8/85/Fushimi_Inari-taisha_Senbon_Torii.jpg',
        },
    ],
    'afghanistan': [
        {
            'name_fa': 'دریاچه‌های بند امیر', 'name_en': 'Band-e-Amir Lakes',
            'summary_fa': 'نخستین پارک ملی افغانستان با مجموعه‌ای از دریاچه‌های آبی خیره‌کننده.',
            'summary_en': 'Afghanistan\'s first national park, home to a chain of stunning turquoise lakes.',
            'description_fa': 'بند امیر در استان بامیان، مجموعه‌ای از شش دریاچه‌ی به‌هم‌پیوسته با آبی به‌رنگ فیروزه‌ای است که با سدهای طبیعی آهکی از هم جدا شده‌اند.',
            'description_en': 'Located in Bamyan province, Band-e-Amir is a chain of six connected turquoise lakes separated by natural travertine dams.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2a/Band-e-Amir_National_Park.jpg',
        },
    ],
}

# (origin_slug, destination_slug, mode, distance_km, duration_text_fa, duration_text_en)
ROUTES = [
    ('turkey', 'iran', 'air', 2200, 'حدود ۳ ساعت پرواز مستقیم', 'About 3 hours direct flight'),
    ('turkey', 'iran', 'land', 2600, 'حدود ۳۰ تا ۳۵ ساعت رانندگی', 'About 30-35 hours by road'),
    ('iran', 'turkey', 'air', 2200, 'حدود ۳ ساعت پرواز مستقیم', 'About 3 hours direct flight'),
    ('iran', 'turkey', 'land', 2600, 'حدود ۳۰ تا ۳۵ ساعت رانندگی', 'About 30-35 hours by road'),
    ('afghanistan', 'iran', 'air', 1100, 'حدود ۱ ساعت و ۴۵ دقیقه پرواز مستقیم', 'About 1h45m direct flight'),
    ('afghanistan', 'iran', 'land', 1400, 'حدود ۲۰ تا ۲۴ ساعت رانندگی', 'About 20-24 hours by road'),
    ('iran', 'afghanistan', 'air', 1100, 'حدود ۱ ساعت و ۴۵ دقیقه پرواز مستقیم', 'About 1h45m direct flight'),
    ('iran', 'afghanistan', 'land', 1400, 'حدود ۲۰ تا ۲۴ ساعت رانندگی', 'About 20-24 hours by road'),
    ('iran', 'japan', 'air', 7500, 'حدود ۱۲ تا ۱۵ ساعت پرواز (با یک توقف)', 'About 12-15 hours (one stop)'),
    ('japan', 'iran', 'air', 7500, 'حدود ۱۲ تا ۱۵ ساعت پرواز (با یک توقف)', 'About 12-15 hours (one stop)'),
    ('turkey', 'japan', 'air', 8900, 'حدود ۱۲ ساعت پرواز مستقیم', 'About 12 hours direct flight'),
    ('japan', 'turkey', 'air', 8900, 'حدود ۱۲ ساعت پرواز مستقیم', 'About 12 hours direct flight'),
]


def seed(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    Attraction = apps.get_model('core', 'Attraction')
    TravelRoute = apps.get_model('core', 'TravelRoute')

    country_objs = {}
    for slug, data in COUNTRIES.items():
        country, created = Country.objects.get_or_create(
            slug=slug,
            defaults={
                'name': data['name_fa'],
                'name_fa': data['name_fa'],
                'name_en': data['name_en'],
                'description': data['description_fa'],
                'description_fa': data['description_fa'],
                'description_en': data['description_en'],
                'background_image_url': data['background_image_url'],
            },
        )
        if not created and not country.background_image_url:
            country.background_image_url = data['background_image_url']
            country.save(update_fields=['background_image_url'])
        country_objs[slug] = country

    for slug, attractions in ATTRACTIONS.items():
        country = country_objs[slug]
        for order, attraction_data in enumerate(attractions):
            Attraction.objects.get_or_create(
                country=country,
                slug=attraction_data['name_en'].lower().replace(' ', '-').replace(',', ''),
                defaults={
                    'name': attraction_data['name_fa'],
                    'name_fa': attraction_data['name_fa'],
                    'name_en': attraction_data['name_en'],
                    'summary': attraction_data['summary_fa'],
                    'summary_fa': attraction_data['summary_fa'],
                    'summary_en': attraction_data['summary_en'],
                    'description': attraction_data['description_fa'],
                    'description_fa': attraction_data['description_fa'],
                    'description_en': attraction_data['description_en'],
                    'image_url': attraction_data['image_url'],
                    'order': order,
                },
            )

    for origin_slug, dest_slug, mode, distance_km, duration_fa, duration_en in ROUTES:
        TravelRoute.objects.get_or_create(
            origin_country=country_objs[origin_slug],
            destination_country=country_objs[dest_slug],
            mode=mode,
            defaults={
                'distance_km': distance_km,
                'duration_text': duration_fa,
                'duration_text_fa': duration_fa,
                'duration_text_en': duration_en,
            },
        )


def unseed(apps, schema_editor):
    # Deliberately a no-op: reversing would delete real admin data if any
    # of these rows were later edited/expanded by hand, and there's no
    # reliable way to tell "still exactly what this migration created"
    # apart from "an admin has since customized it". Same reasoning as the
    # other seed migrations in this project.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_attraction_travelroute'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
