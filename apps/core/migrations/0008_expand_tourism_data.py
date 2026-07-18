from django.db import migrations

# Second data pass, in direct response to feedback: (1) far too few
# attractions per country (Afghanistan had only one!) — this adds 2-4 more
# real, well-known attractions to each of the four countries already
# seeded, with real names/descriptions researched the same way any
# tourism site would present them; (2) extends coverage to four more
# major countries already in the Country list (Pakistan, UAE, Saudi
# Arabia, India) with their own attractions + real travel routes to/from
# Iran, since a purely Iran-anchored calculator is what's actually useful
# for this site's audience. This is STILL a demonstration subset, not all
# 36 countries — see the accompanying user-facing note.

EXTRA_ATTRACTIONS = {
    'iran': [
        {
            'name_fa': 'کاخ گلستان', 'name_en': 'Golestan Palace',
            'summary_fa': 'کهن‌ترین مجموعه‌ی تاریخی تهران و باقی‌مانده‌ی ارگ سلطنتی دوره‌ی قاجار.',
            'summary_en': 'Tehran\'s oldest historic complex, the surviving royal citadel of the Qajar era.',
            'description_fa': 'کاخ گلستان با تالارهای آینه‌کاری‌شده و کاشی‌های هفت‌رنگ، نمونه‌ای برجسته از هنر و معماری دوره‌ی قاجار و ثبت‌شده در فهرست میراث جهانی یونسکو است.',
            'description_en': 'With mirrored halls and haft-rang tilework, Golestan Palace is an outstanding example of Qajar-era art and architecture and a UNESCO World Heritage Site.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6c/Golestan_Palace2.JPG',
        },
        {
            'name_fa': 'برج آزادی', 'name_en': 'Azadi Tower',
            'summary_fa': 'نماد شهر تهران، بنایی سفید با ترکیبی از معماری هخامنشی و ساسانی.',
            'summary_en': 'The symbol of Tehran, a white monument blending Achaemenid and Sassanid architectural motifs.',
            'description_fa': 'برج آزادی در میدان آزادی تهران، از سنگ مرمر سفید ساخته شده و ترکیبی از عناصر معماری پیش از اسلام ایران را در طرحی مدرن به نمایش می‌گذارد.',
            'description_en': 'Standing in Tehran\'s Azadi Square and built from white marble, the tower reinterprets pre-Islamic Persian architectural elements in a modern design.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6a/Azadi_Tower_2016.jpg',
        },
        {
            'name_fa': 'دریاچه ارومیه', 'name_en': 'Lake Urmia',
            'summary_fa': 'یکی از بزرگ‌ترین دریاچه‌های آب‌شور جهان در شمال‌غرب ایران.',
            'summary_en': 'One of the world\'s largest saltwater lakes, in northwestern Iran.',
            'description_fa': 'دریاچه ارومیه با آب صورتی‌رنگ در برخی فصول و جزایر متعدد، یکی از چشم‌اندازهای طبیعی خاص ایران و زیستگاه پرندگان مهاجر است.',
            'description_en': 'With its seasonally pink-tinted water and many islands, Lake Urmia is one of Iran\'s most distinctive natural landscapes and a habitat for migratory birds.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/1/16/Lake_Urmia_from_space.jpg',
        },
    ],
    'afghanistan': [
        {
            'name_fa': 'مسجد کبود مزار شریف', 'name_en': 'Blue Mosque, Mazar-i-Sharif',
            'summary_fa': 'زیارتگاه و مسجدی با کاشی‌کاری‌های آبی خیره‌کننده، از نمادهای مذهبی افغانستان.',
            'summary_en': 'A shrine and mosque famed for its dazzling blue tilework, one of Afghanistan\'s religious landmarks.',
            'description_fa': 'مسجد کبود که به نام روضه شریف نیز شناخته می‌شود، با گنبدها و کاشی‌های فیروزه‌ای و آبی، یکی از زیباترین بناهای مذهبی آسیای مرکزی است.',
            'description_en': 'Also known as the Rawze-i-Sharif, the Blue Mosque with its turquoise and blue-tiled domes is one of the most beautiful religious buildings in Central Asia.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6a/Mazari_sharif_shrine.jpg',
        },
        {
            'name_fa': 'منارجام', 'name_en': 'Minaret of Jam',
            'summary_fa': 'مناره‌ای آجری از قرن دوازدهم میلادی، ثبت‌شده در میراث جهانی یونسکو.',
            'summary_en': 'A 12th-century brick minaret and UNESCO World Heritage Site.',
            'description_fa': 'منارجام در دره‌ای دورافتاده در ولایت غور قرار دارد و با ارتفاع نزدیک به ۶۵ متر، دومین مناره‌ی بلند آجری جهان و یادگاری از دوره‌ی غوریان است.',
            'description_en': 'Standing in a remote valley in Ghor province, the roughly 65-metre Minaret of Jam is the second-tallest brick minaret in the world and a relic of the Ghurid era.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/94/Minaret_of_Jam_1976.jpg',
        },
        {
            'name_fa': 'دره واخان', 'name_en': 'Wakhan Corridor',
            'summary_fa': 'باریکه‌ای کوهستانی در شرق افغانستان با طبیعتی بکر و مسیرهای کوه‌نوردی.',
            'summary_en': 'A remote mountainous strip in eastern Afghanistan with pristine nature and trekking routes.',
            'description_fa': 'دره واخان با کوه‌های پامیر و هندوکش، دام‌داران کوچ‌رو قرقیزی و طبیعتی دست‌نخورده، مقصدی برای گردشگری ماجراجویانه و کوه‌نوردی است.',
            'description_en': 'Framed by the Pamir and Hindu Kush ranges, home to nomadic Kyrgyz herders and largely untouched nature, the Wakhan Corridor is a destination for adventure trekking.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/97/Wakhan_Corridor_Landscape.jpg',
        },
    ],
    'turkey': [
        {
            'name_fa': 'پاموک‌کاله', 'name_en': 'Pamukkale',
            'summary_fa': 'تراس‌های سفید آهکی و چشمه‌های آب‌گرم طبیعی در جنوب‌غرب ترکیه.',
            'summary_en': 'Brilliant white travertine terraces and natural hot springs in southwestern Turkey.',
            'description_fa': 'پاموک‌کاله به معنای «قلعه پنبه‌ای»، مجموعه‌ای از تراس‌های سفید آهکی است که آب‌های گرم معدنی طی هزاران سال آن را شکل داده‌اند؛ در کنارش شهر باستانی هیراپولیس نیز قرار دارد.',
            'description_en': 'Meaning "cotton castle," Pamukkale is a series of white travertine terraces shaped over millennia by mineral-rich hot springs, sitting alongside the ancient city of Hierapolis.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/45/Pamukkale_Turkey.jpg',
        },
        {
            'name_fa': 'افسوس (اِفِسوس)', 'name_en': 'Ephesus',
            'summary_fa': 'یکی از بهترین شهرهای باستانی حفظ‌شده‌ی یونانی-رومی در جهان.',
            'summary_en': 'One of the best-preserved ancient Greco-Roman cities in the world.',
            'description_fa': 'افسوس با کتابخانه‌ی سلسیوس، تئاتر بزرگ و خیابان‌های سنگ‌فرش‌شده، تصویری زنده از زندگی شهری دوران روم باستان ارائه می‌دهد.',
            'description_en': 'With the Library of Celsus, the great theatre, and its paved streets, Ephesus offers a vivid picture of urban life in the Roman era.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/7/7a/Ephesus_Celsus_Library_Facade.jpg',
        },
    ],
    'japan': [
        {
            'name_fa': 'معبد کینکاکوجی (کاخ زرین)', 'name_en': 'Kinkaku-ji (Golden Pavilion)',
            'summary_fa': 'معبدی زرین‌پوش در کیوتو که تصویرش در آب دریاچه‌ی مقابلش منعکس می‌شود.',
            'summary_en': 'A gold-leaf-covered Kyoto temple whose reflection shimmers in the pond before it.',
            'description_fa': 'کینکاکوجی با نمای پوشیده از ورق طلا و باغ ژاپنی اطرافش، یکی از نمادی‌ترین و پربازدیدترین بناهای کیوتو است.',
            'description_en': 'Covered in gold leaf and set within a classic Japanese garden, Kinkaku-ji is one of Kyoto\'s most iconic and visited landmarks.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/f/f6/Kinkaku-ji_2007.jpg',
        },
        {
            'name_fa': 'معبد ایتسوکوشیما (میاجیما)', 'name_en': 'Itsukushima Shrine (Miyajima)',
            'summary_fa': 'معبد شناور با دروازه‌ی توری بزرگ که هنگام جزر و مد در آب دریا شناور به‌نظر می‌رسد.',
            'summary_en': 'A shrine with a giant floating torii gate that appears to hover over the sea at high tide.',
            'description_fa': 'معبد ایتسوکوشیما در جزیره‌ی میاجیما، با دروازه‌ی توری نارنجی‌رنگش که هنگام جزر و مد به‌نظر شناور می‌آید، یکی از سه منظره‌ی برتر ژاپن شناخته می‌شود.',
            'description_en': 'On Miyajima Island, with its vermillion torii gate that seems to float at high tide, Itsukushima Shrine is regarded as one of Japan\'s three most scenic views.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/9c/Miyajima_Itsukushima_Torii_Sunset_9-2-2004_%285%29.jpg',
        },
    ],
}

NEW_COUNTRY_ATTRACTIONS = {
    'pakistan': [
        {
            'name_fa': 'مسجد بادشاهی لاهور', 'name_en': 'Badshahi Mosque, Lahore',
            'summary_fa': 'یکی از بزرگ‌ترین مساجد دوران مغول در جهان.',
            'summary_en': 'One of the largest Mughal-era mosques in the world.',
            'description_fa': 'مسجد بادشاهی در لاهور، ساخته‌شده در دوران اورنگ‌زیب، با حیاطی وسیع و کاشی‌کاری‌های سرخ و سفید، نمونه‌ای برجسته از معماری مغولی است.',
            'description_en': 'Built during the reign of Aurangzeb, Lahore\'s Badshahi Mosque with its vast courtyard and red-and-white tilework is an outstanding example of Mughal architecture.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/95/Badshahi_Mosque_Full_View.JPG',
        },
        {
            'name_fa': 'دره هونزا', 'name_en': 'Hunza Valley',
            'summary_fa': 'دره‌ای کوهستانی خیره‌کننده در شمال پاکستان، محاطه‌شده با قله‌های برفی.',
            'summary_en': 'A breathtaking mountain valley in northern Pakistan, ringed by snow-capped peaks.',
            'description_fa': 'دره هونزا با باغ‌های میوه، رودخانه‌های یخچالی و چشم‌اندازی از قله‌های راکاپوشی، یکی از زیباترین مقاصد گردشگری کوهستانی جهان است.',
            'description_en': 'With its orchards, glacial rivers, and views of Rakaposhi peak, Hunza Valley is one of the world\'s most beautiful mountain tourism destinations.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/7/7f/Hunza_Valley_Pakistan.jpg',
        },
    ],
    'united-arab-emirates': [
        {
            'name_fa': 'برج خلیفه دبی', 'name_en': 'Burj Khalifa, Dubai',
            'summary_fa': 'بلندترین ساختمان جهان و نماد مدرن شهر دبی.',
            'summary_en': 'The tallest building in the world and the modern symbol of Dubai.',
            'description_fa': 'برج خلیفه با ارتفاع بیش از ۸۲۸ متر، دارای سکوهای مشاهده‌ی عمومی است که چشم‌اندازی بی‌نظیر از شهر دبی و کویرهای اطرافش ارائه می‌دهد.',
            'description_en': 'Standing over 828 metres tall, Burj Khalifa has public observation decks offering unmatched views over Dubai and the surrounding desert.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/1/15/Burj_Khalifa.jpg',
        },
        {
            'name_fa': 'مسجد جامع شیخ زاید', 'name_en': 'Sheikh Zayed Grand Mosque',
            'summary_fa': 'یکی از بزرگ‌ترین و زیباترین مساجد جهان در ابوظبی.',
            'summary_en': 'One of the largest and most beautiful mosques in the world, in Abu Dhabi.',
            'description_fa': 'مسجد جامع شیخ زاید با گنبدهای سفید مرمرین، بزرگ‌ترین فرش دست‌بافت جهان و لوسترهای کریستالی، جاذبه‌ای معماری و معنوی برجسته است.',
            'description_en': 'With its white marble domes, the world\'s largest hand-woven carpet, and crystal chandeliers, Sheikh Zayed Grand Mosque is a landmark of both architecture and spirituality.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/b/b6/Sheikh_Zayed_Mosque_2019.jpg',
        },
    ],
    'saudi-arabia': [
        {
            'name_fa': 'مدائن صالح (الحجر) - العلا', 'name_en': 'Madain Saleh (Al-Hijr), AlUla',
            'summary_fa': 'شهر باستانی نبطی با آرامگاه‌های سنگی تراش‌خورده، اولین میراث جهانی یونسکو در عربستان.',
            'summary_en': 'An ancient Nabataean city of rock-cut tombs, Saudi Arabia\'s first UNESCO World Heritage Site.',
            'description_fa': 'مدائن صالح در نزدیکی العلا، خواهرشهر پترای اردن است و شامل ده‌ها آرامگاه تراش‌خورده در صخره‌های ماسه‌سنگی از دوران نبطیان است.',
            'description_en': 'Near AlUla, Madain Saleh is the sister site to Jordan\'s Petra, featuring dozens of tombs carved into sandstone cliffs by the Nabataeans.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/48/Mada%27in_Saleh_02.jpg',
        },
    ],
    'india': [
        {
            'name_fa': 'تاج محل', 'name_en': 'Taj Mahal',
            'summary_fa': 'بنای سفید مرمرین در آگرا، نمادی جهانی از عشق و معماری مغولی.',
            'summary_en': 'A white marble mausoleum in Agra, a global symbol of love and Mughal architecture.',
            'description_fa': 'تاج محل به دستور شاه‌جهان و در یادبود همسرش ممتاز محل ساخته شد و با تقارن کامل و کاشی‌کاری‌های ظریفش، یکی از هفت عجایب جهان نو است.',
            'description_en': 'Built by Shah Jahan in memory of his wife Mumtaz Mahal, the Taj Mahal\'s perfect symmetry and intricate inlay work make it one of the New Seven Wonders of the World.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/64/Taj_Mahal%2C_Agra%2C_India_edit3.jpg',
        },
        {
            'name_fa': 'قلعه آمبر جیپور', 'name_en': 'Amber Fort, Jaipur',
            'summary_fa': 'قلعه‌ای باشکوه از سنگ ماسه‌ای و مرمر بر فراز تپه‌ای در جیپور.',
            'summary_en': 'A magnificent sandstone-and-marble fort perched on a hill in Jaipur.',
            'description_fa': 'قلعه آمبر با تالار آینه‌ها، حیاط‌های وسیع و چشم‌اندازی رو به دریاچه‌ی مووتا، یکی از مهم‌ترین جاذبه‌های «شهر صورتی» جیپور است.',
            'description_en': 'With its Hall of Mirrors, vast courtyards, and views over Maota Lake, Amber Fort is one of the key attractions of Jaipur, the "Pink City".',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/63/Amber_Fort_Jaipur.jpg',
        },
    ],
}

# (origin_slug, destination_slug, mode, distance_km, duration_fa, duration_en)
NEW_ROUTES = [
    ('iran', 'pakistan', 'air', 1500, 'حدود ۲ ساعت پرواز مستقیم', 'About 2 hours direct flight'),
    ('pakistan', 'iran', 'air', 1500, 'حدود ۲ ساعت پرواز مستقیم', 'About 2 hours direct flight'),
    ('iran', 'pakistan', 'land', 1700, 'حدود ۲۴ تا ۳۰ ساعت رانندگی (مرز میرجاوه-تفتان)', 'About 24-30 hours by road (Mirjaveh-Taftan border)'),
    ('pakistan', 'iran', 'land', 1700, 'حدود ۲۴ تا ۳۰ ساعت رانندگی (مرز میرجاوه-تفتان)', 'About 24-30 hours by road (Mirjaveh-Taftan border)'),
    ('iran', 'united-arab-emirates', 'air', 700, 'حدود ۱ ساعت و ۳۰ دقیقه پرواز مستقیم', 'About 1h30m direct flight'),
    ('united-arab-emirates', 'iran', 'air', 700, 'حدود ۱ ساعت و ۳۰ دقیقه پرواز مستقیم', 'About 1h30m direct flight'),
    ('iran', 'united-arab-emirates', 'sea', 300, 'حدود ۶ تا ۸ ساعت با کشتی مسافربری (بندرعباس/بندرلنگه به دبی/شارجه)', 'About 6-8 hours by ferry (Bandar Abbas/Lengeh to Dubai/Sharjah)'),
    ('united-arab-emirates', 'iran', 'sea', 300, 'حدود ۶ تا ۸ ساعت با کشتی مسافربری', 'About 6-8 hours by ferry'),
    ('iran', 'saudi-arabia', 'air', 1900, 'حدود ۳ ساعت پرواز مستقیم', 'About 3 hours direct flight'),
    ('saudi-arabia', 'iran', 'air', 1900, 'حدود ۳ ساعت پرواز مستقیم', 'About 3 hours direct flight'),
    ('iran', 'india', 'air', 2700, 'حدود ۴ ساعت و ۳۰ دقیقه پرواز مستقیم', 'About 4h30m direct flight'),
    ('india', 'iran', 'air', 2700, 'حدود ۴ ساعت و ۳۰ دقیقه پرواز مستقیم', 'About 4h30m direct flight'),
]


def seed(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    Attraction = apps.get_model('core', 'Attraction')
    TravelRoute = apps.get_model('core', 'TravelRoute')

    def add_attractions(slug, items, start_order):
        try:
            country = Country.objects.get(slug=slug)
        except Country.DoesNotExist:
            return
        for i, data in enumerate(items):
            slug_val = data['name_en'].lower().replace(' ', '-').replace(',', '').replace('(', '').replace(')', '')
            Attraction.objects.get_or_create(
                country=country,
                slug=slug_val,
                defaults={
                    'name': data['name_fa'],
                    'name_fa': data['name_fa'],
                    'name_en': data['name_en'],
                    'summary': data['summary_fa'],
                    'summary_fa': data['summary_fa'],
                    'summary_en': data['summary_en'],
                    'description': data['description_fa'],
                    'description_fa': data['description_fa'],
                    'description_en': data['description_en'],
                    'image_url': data['image_url'],
                    'order': start_order + i,
                },
            )

    for slug, items in EXTRA_ATTRACTIONS.items():
        add_attractions(slug, items, start_order=10)

    for slug, items in NEW_COUNTRY_ATTRACTIONS.items():
        add_attractions(slug, items, start_order=0)

    countries_by_slug = {}

    def get_country(slug):
        if slug not in countries_by_slug:
            countries_by_slug[slug] = Country.objects.filter(slug=slug).first()
        return countries_by_slug[slug]

    for origin_slug, dest_slug, mode, distance_km, duration_fa, duration_en in NEW_ROUTES:
        origin = get_country(origin_slug)
        dest = get_country(dest_slug)
        if not origin or not dest:
            continue
        TravelRoute.objects.get_or_create(
            origin_country=origin,
            destination_country=dest,
            mode=mode,
            defaults={
                'distance_km': distance_km,
                'duration_text': duration_fa,
                'duration_text_fa': duration_fa,
                'duration_text_en': duration_en,
            },
        )


def unseed(apps, schema_editor):
    # No-op — same reasoning as 0007_seed_attractions_travelroutes.py.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_seed_attractions_travelroutes'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
