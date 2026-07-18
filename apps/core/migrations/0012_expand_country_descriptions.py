from django.db import migrations

# The Country.description written when these 8 countries were first
# seeded/touched was only 1-2 sentences — nowhere near enough for a
# country landing page. This replaces it with several real paragraphs
# per country (geography, history, culture/economy) in both languages.

DESCRIPTIONS = {
    'iran': {
        'fa': (
            'ایران، با نام رسمی جمهوری اسلامی ایران، کشوری در غرب آسیا با بیش از هشت هزار سال قدمت تمدنی است. '
            'این سرزمین از شمال به دریای خزر، از جنوب به خلیج فارس و دریای عمان، و از همسایگانی چون ترکیه، عراق، '
            'ارمنستان، آذربایجان، ترکمنستان، افغانستان و پاکستان احاطه شده است. تنوع جغرافیایی ایران خیره‌کننده '
            'است: از قله‌های برف‌گیر البرز و زاگرس تا کویرهای وسیع مرکزی، از جنگل‌های سرسبز شمال تا سواحل گرمسیری '
            'جنوب.\n\n'
            'تاریخ ایران با امپراتوری‌های بزرگی چون هخامنشیان، اشکانیان و ساسانیان گره خورده که میراث آن‌ها، از '
            'تخت جمشید تا کاخ‌های اصفهان، امروز بخشی از میراث جهانی بشریت به‌شمار می‌رود. زبان فارسی، شعر حافظ و '
            'سعدی و فردوسی، و معماری اسلامی-ایرانی مساجد و کاخ‌ها، تصویری از عمق فرهنگی این سرزمین ارائه می‌دهند.\n\n'
            'امروزه ایران با جمعیتی حدود ۸۵ میلیون نفر، اقتصادی متکی بر نفت و گاز، کشاورزی و صنایع دستی دارد و '
            'شهرهایی چون تهران (پایتخت)، اصفهان، شیراز، مشهد و یزد از مقاصد اصلی گردشگری داخلی و خارجی این کشور '
            'هستند.'
        ),
        'en': (
            'Iran, officially the Islamic Republic of Iran, is a West Asian country with more than eight thousand '
            'years of civilizational history. It borders the Caspian Sea to the north, the Persian Gulf and the '
            'Gulf of Oman to the south, and neighbors including Turkey, Iraq, Armenia, Azerbaijan, Turkmenistan, '
            'Afghanistan, and Pakistan. Iran\'s geography is remarkably diverse: from the snow-capped peaks of the '
            'Alborz and Zagros ranges to the vast central deserts, from the lush forests of the north to the '
            'tropical coastline of the south.\n\n'
            'Iran\'s history is tied to great empires such as the Achaemenids, Parthians, and Sassanids, whose '
            'legacy — from Persepolis to the palaces of Isfahan — is now part of humanity\'s shared world heritage. '
            'The Persian language, the poetry of Hafez, Saadi, and Ferdowsi, and the Islamic-Persian architecture '
            'of its mosques and palaces all reflect the cultural depth of this land.\n\n'
            'Today, Iran has a population of roughly 85 million, an economy built on oil and gas, agriculture, and '
            'handicrafts, and cities such as Tehran (the capital), Isfahan, Shiraz, Mashhad, and Yazd stand among '
            'the country\'s main destinations for domestic and international tourism.'
        ),
    },
    'afghanistan': {
        'fa': (
            'افغانستان کشوری کوهستانی و محصور در خشکی در آسیای مرکزی-جنوبی است که در طول تاریخ به‌عنوان «چهارراه '
            'آسیا» و بخشی از جاده ابریشم، محل تلاقی تمدن‌های ایرانی، هندی، آسیای مرکزی و چین بوده است. این کشور با '
            'ایران، ترکمنستان، ازبکستان، تاجیکستان، چین و پاکستان هم‌مرز است و کوه‌های هندوکش بخش بزرگی از پستی و '
            'بلندی آن را شکل می‌دهند.\n\n'
            'تاریخ افغانستان شامل دوره‌های امپراتوری‌های کوشانی، غزنوی، غوری و تیموری است و آثاری چون منارجام و '
            'یادگارهای بودایی بامیان (که امروز تنها به‌صورت تاریخی و در قالب عکس باقی مانده‌اند) گواه این گذشته‌ی '
            'پرفراز و نشیب‌اند. فرهنگ افغانستان ترکیبی از قومیت‌های پشتون، تاجیک، هزاره، ازبک و دیگر اقوام است که '
            'هرکدام زبان، موسیقی و آداب‌ورسوم خاص خود را دارند.\n\n'
            'طبیعت افغانستان، از دریاچه‌های فیروزه‌ای بند امیر در بامیان تا دره‌های مرتفع واخان در شرق کشور، '
            'جاذبه‌هایی کمتر شناخته‌شده اما خیره‌کننده برای گردشگری طبیعت و ماجراجویی فراهم می‌کند. کابل به‌عنوان '
            'پایتخت، و شهرهایی چون مزار شریف، هرات و قندهار از مراکز مهم تاریخی و فرهنگی این کشورند.'
        ),
        'en': (
            'Afghanistan is a mountainous, landlocked country in South-Central Asia that has historically served '
            'as the "crossroads of Asia" and a key link on the Silk Road, where Persian, Indian, Central Asian, '
            'and Chinese civilizations met. It borders Iran, Turkmenistan, Uzbekistan, Tajikistan, China, and '
            'Pakistan, with the Hindu Kush mountains shaping much of its terrain.\n\n'
            'Afghanistan\'s history spans the Kushan, Ghaznavid, Ghurid, and Timurid empires, and sites such as '
            'the Minaret of Jam and the historic Buddhas of Bamyan (which now survive only in historical record '
            'and photographs) bear witness to this eventful past. Afghan culture is a blend of Pashtun, Tajik, '
            'Hazara, Uzbek, and other ethnic communities, each with its own language, music, and customs.\n\n'
            'Afghanistan\'s nature, from the turquoise lakes of Band-e-Amir in Bamyan to the high valleys of the '
            'Wakhan Corridor in the east, offers lesser-known but striking destinations for nature and adventure '
            'tourism. Kabul, the capital, along with cities such as Mazar-i-Sharif, Herat, and Kandahar, are '
            'important historical and cultural centers of the country.'
        ),
    },
    'turkey': {
        'fa': (
            'ترکیه کشوری میان‌قاره‌ای است که بخش عمده‌ی آن در آناتولی (آسیای صغیر) و بخش کوچکی در جنوب‌شرق اروپا '
            'قرار دارد؛ همین موقعیت، ترکیه را به‌طور تاریخی و فرهنگی پلی میان شرق و غرب تبدیل کرده است. این کشور '
            'با دریای سیاه، دریای اژه و دریای مدیترانه هم‌مرز است و همسایگانی چون یونان، بلغارستان، گرجستان، '
            'ارمنستان، ایران، عراق و سوریه دارد.\n\n'
            'استانبول، تنها کلان‌شهر جهان که هم‌زمان در دو قاره قرار گرفته، روزگاری پایتخت امپراتوری‌های روم '
            'شرقی (بیزانس) و عثمانی بوده و بناهایی چون ایاصوفیه و کاخ توپکاپی یادگار آن دوران‌اند. آنکارا امروز '
            'پایتخت سیاسی ترکیه است. مناطقی چون کاپادوکیا با دودکش‌های پریان و شهرهای زیرزمینی، و پاموک‌کاله با '
            'تراس‌های سفید آهکی‌اش، از شگفت‌انگیزترین چشم‌اندازهای طبیعی جهان به‌شمار می‌روند.\n\n'
            'ترکیه اقتصادی متنوع مبتنی بر گردشگری، صنعت، نساجی و کشاورزی دارد و یکی از پربازدیدترین مقاصد '
            'گردشگری جهان است؛ سواحل مدیترانه‌ای و اژه‌ای آن هرساله میزبان میلیون‌ها گردشگر از سراسر جهان هستند.'
        ),
        'en': (
            'Turkey is a transcontinental country, with most of its territory in Anatolia (Asia Minor) and a '
            'smaller portion in southeastern Europe — a position that has historically and culturally made it a '
            'bridge between East and West. It borders the Black Sea, the Aegean Sea, and the Mediterranean, and '
            'neighbors including Greece, Bulgaria, Georgia, Armenia, Iran, Iraq, and Syria.\n\n'
            'Istanbul, the world\'s only megacity spanning two continents, was once the capital of both the '
            'Byzantine and Ottoman empires, and landmarks such as the Hagia Sophia and Topkapi Palace remain from '
            'that era. Ankara is today Turkey\'s political capital. Regions such as Cappadocia, with its fairy '
            'chimneys and underground cities, and Pamukkale, with its white travertine terraces, rank among the '
            'world\'s most extraordinary natural landscapes.\n\n'
            'Turkey has a diverse economy built on tourism, industry, textiles, and agriculture, and is one of the '
            'world\'s most visited tourist destinations; its Mediterranean and Aegean coastlines welcome millions '
            'of visitors from around the world every year.'
        ),
    },
    'japan': {
        'fa': (
            'ژاپن کشوری جزیره‌ای در شرق آسیا است که از چهار جزیره‌ی اصلی هوکایدو، هونشو، شیکوکو و کیوشو و هزاران '
            'جزیره‌ی کوچک‌تر تشکیل شده و در اقیانوس آرام، در همسایگی کره جنوبی، کره شمالی، چین و روسیه قرار دارد. '
            'کوه فوجی، بلندترین قله‌ی این کشور، نماد ملی و معنوی ژاپن به‌شمار می‌رود.\n\n'
            'تاریخ ژاپن با دوره‌های امپراتوری، حکومت شوگون‌ها و سامورایی‌ها، و سپس نوسازی سریع دوران میجی گره '
            'خورده است. این کشور امروز ترکیبی بی‌نظیر از سنت و فناوری پیشرفته را به نمایش می‌گذارد: در کنار معابد '
            'باستانی کیوتو مانند کینکاکوجی و فوشیمی‌ایناری، شهرهایی چون توکیو با فناوری و معماری مدرن خود می‌درخشند.\n\n'
            'فرهنگ ژاپن با آیین‌های چای، هنر ایکبانا، تئاتر سنتی کابوکی و نو، آشپزی ظریف و فصل شکوفه‌های گیلاس '
            '(هانامی) شناخته می‌شود. ژاپن با جمعیتی نزدیک به ۱۲۵ میلیون نفر، سومین اقتصاد بزرگ جهان و پیشرو در '
            'صنایع خودروسازی، الکترونیک و فناوری است.'
        ),
        'en': (
            'Japan is an island nation in East Asia made up of four main islands — Hokkaido, Honshu, Shikoku, and '
            'Kyushu — along with thousands of smaller islands, located in the Pacific Ocean near South Korea, '
            'North Korea, China, and Russia. Mount Fuji, the country\'s tallest peak, is a national and spiritual '
            'symbol of Japan.\n\n'
            'Japan\'s history spans imperial eras, the rule of shoguns and samurai, and the rapid modernization of '
            'the Meiji period. Today the country presents a unique blend of tradition and advanced technology: '
            'alongside Kyoto\'s ancient temples such as Kinkaku-ji and Fushimi Inari, cities like Tokyo shine with '
            'modern technology and architecture.\n\n'
            'Japanese culture is known for its tea ceremonies, ikebana flower arranging, traditional Kabuki and Noh '
            'theater, refined cuisine, and cherry blossom season (hanami). With a population of nearly 125 '
            'million, Japan is the world\'s third-largest economy and a leader in the automotive, electronics, and '
            'technology industries.'
        ),
    },
    'pakistan': {
        'fa': (
            'پاکستان کشوری در جنوب آسیا با دسترسی به دریای عرب است که با ایران، افغانستان، چین و هند هم‌مرز است. '
            'این کشور از دشت‌های حاصلخیز رود سند تا قله‌های بلند قراقروم و هیمالیا (از جمله کی‌تو، دومین قله‌ی '
            'بلند جهان) تنوع جغرافیایی چشمگیری دارد.\n\n'
            'پاکستان زادگاه یکی از کهن‌ترین تمدن‌های بشری، تمدن دره‌ی سند، است و در طول تاریخ میزبان امپراتوری‌های '
            'مغول، غزنوی و دیگر حکومت‌های اسلامی بوده که میراث معماری آن‌ها، از جمله مسجد بادشاهی لاهور، امروز '
            'همچنان پابرجاست. لاهور به‌عنوان مرکز فرهنگی و کراچی به‌عنوان بزرگ‌ترین شهر و مرکز اقتصادی کشور '
            'شناخته می‌شوند.\n\n'
            'مناطق شمالی پاکستان مانند دره‌ی هونزا و گیلگیت-بلتستان با چشم‌اندازهای کوهستانی خیره‌کننده، مقصد '
            'محبوب کوه‌نوردان و طبیعت‌گردان از سراسر جهان است. پاکستان با جمعیتی بیش از ۲۴۰ میلیون نفر، یکی از '
            'پرجمعیت‌ترین کشورهای جهان و اقتصادی متکی بر کشاورزی، نساجی و خدمات دارد.'
        ),
        'en': (
            'Pakistan is a South Asian country with access to the Arabian Sea, bordering Iran, Afghanistan, China, '
            'and India. It has striking geographic diversity, from the fertile plains of the Indus River to the '
            'towering peaks of the Karakoram and Himalayan ranges, including K2, the world\'s second-highest '
            'mountain.\n\n'
            'Pakistan is home to one of humanity\'s oldest civilizations, the Indus Valley Civilization, and has '
            'historically hosted Mughal, Ghaznavid, and other Islamic empires whose architectural legacy — '
            'including the Badshahi Mosque in Lahore — still stands today. Lahore is known as the country\'s '
            'cultural center, while Karachi is its largest city and economic hub.\n\n'
            'Northern regions such as Hunza Valley and Gilgit-Baltistan, with their stunning mountain scenery, are '
            'popular destinations for mountaineers and nature travelers from around the world. With a population '
            'of over 240 million, Pakistan is one of the world\'s most populous countries, with an economy built '
            'on agriculture, textiles, and services.'
        ),
    },
    'united-arab-emirates': {
        'fa': (
            'امارات متحده عربی فدراسیونی متشکل از هفت امیرنشین (ابوظبی، دبی، شارجه، عجمان، ام‌القیوین، فجیره و '
            'راس‌الخیمه) در شبه‌جزیره‌ی عربستان است که در سواحل خلیج فارس و خلیج عمان قرار دارد و با عربستان '
            'سعودی و عمان هم‌مرز است. ابوظبی پایتخت سیاسی و دبی بزرگ‌ترین و شناخته‌شده‌ترین شهر این کشور است.\n\n'
            'امارات که پیش‌تر اقتصادی متکی بر صید مروارید و تجارت داشت، از دهه‌ی ۱۹۷۰ با کشف نفت و سرمایه‌گذاری‌های '
            'گسترده، به یکی از مدرن‌ترین و ثروتمندترین کشورهای منطقه تبدیل شده است. برج خلیفه در دبی، بلندترین '
            'ساختمان جهان، و مسجد جامع شیخ زاید در ابوظبی، از نمادهای این تحول‌اند.\n\n'
            'امروز امارات به‌عنوان مرکز تجارت، گردشگری، هوانوردی و امور مالی خاورمیانه شناخته می‌شود و جزایر '
            'مصنوعی، مراکز خرید عظیم و معماری آینده‌نگرانه‌ی آن، سالانه میلیون‌ها گردشگر را جذب می‌کند.'
        ),
        'en': (
            'The United Arab Emirates is a federation of seven emirates — Abu Dhabi, Dubai, Sharjah, Ajman, Umm '
            'Al Quwain, Fujairah, and Ras Al Khaimah — on the Arabian Peninsula, situated along the Persian Gulf '
            'and the Gulf of Oman, bordering Saudi Arabia and Oman. Abu Dhabi is the political capital, while '
            'Dubai is the country\'s largest and best-known city.\n\n'
            'Once an economy built on pearl diving and trade, the UAE transformed from the 1970s onward through '
            'oil discovery and extensive investment into one of the region\'s most modern and wealthiest '
            'countries. Burj Khalifa in Dubai, the tallest building in the world, and the Sheikh Zayed Grand '
            'Mosque in Abu Dhabi, are symbols of this transformation.\n\n'
            'Today the UAE is known as a hub for trade, tourism, aviation, and finance in the Middle East, and its '
            'artificial islands, massive shopping malls, and futuristic architecture draw millions of visitors '
            'every year.'
        ),
    },
    'saudi-arabia': {
        'fa': (
            'عربستان سعودی بزرگ‌ترین کشور شبه‌جزیره‌ی عربستان است که بیشتر مساحت آن را کویر تشکیل می‌دهد و از '
            'خلیج فارس تا دریای سرخ امتداد دارد. این کشور با اردن، عراق، کویت، قطر، امارات، عمان و یمن هم‌مرز '
            'است و میزبان دو شهر مقدس اسلام، مکه و مدینه است.\n\n'
            'هرساله میلیون‌ها مسلمان از سراسر جهان برای انجام فریضه‌ی حج و عمره به مکه سفر می‌کنند و مسجدالحرام، '
            'بزرگ‌ترین مسجد جهان، قلب معنوی این سفرهاست. در سال‌های اخیر، عربستان با طرح‌های بزرگ گردشگری مانند '
            'العلا (میزبان مدائن صالح، شهر باستانی نبطی) تلاش کرده گردشگری غیرمذهبی را نیز گسترش دهد.\n\n'
            'ریاض به‌عنوان پایتخت و مرکز سیاسی، و جده به‌عنوان دروازه‌ی تاریخی حج، از مهم‌ترین شهرهای این کشورند. '
            'اقتصاد عربستان همچنان به‌شدت به صادرات نفت وابسته است، هرچند برنامه‌های توسعه‌ای مانند «چشم‌انداز '
            '۲۰۳۰» در پی متنوع‌سازی آن هستند.'
        ),
        'en': (
            'Saudi Arabia is the largest country on the Arabian Peninsula, mostly covered by desert, stretching '
            'from the Persian Gulf to the Red Sea. It borders Jordan, Iraq, Kuwait, Qatar, the UAE, Oman, and '
            'Yemen, and is home to Islam\'s two holiest cities, Mecca and Medina.\n\n'
            'Every year, millions of Muslims from around the world travel to Mecca to perform Hajj and Umrah, with '
            'the Masjid al-Haram, the world\'s largest mosque, at the spiritual heart of these journeys. In recent '
            'years, Saudi Arabia has pursued major tourism projects such as AlUla (home to Madain Saleh, an '
            'ancient Nabataean city) to expand non-religious tourism as well.\n\n'
            'Riyadh, the capital and political center, and Jeddah, the historic gateway to Hajj, are among the '
            'country\'s most important cities. Saudi Arabia\'s economy remains heavily dependent on oil exports, '
            'though development plans such as "Vision 2030" aim to diversify it.'
        ),
    },
    'india': {
        'fa': (
            'هند دومین کشور پرجمعیت جهان و بزرگ‌ترین دموکراسی دنیاست که در جنوب آسیا قرار دارد و با پاکستان، '
            'چین، نپال، بوتان، بنگلادش و میانمار هم‌مرز است. این کشور از قله‌های هیمالیا در شمال تا سواحل اقیانوس '
            'هند در جنوب، تنوع جغرافیایی و اقلیمی خارق‌العاده‌ای دارد.\n\n'
            'هند زادگاه چند دین بزرگ جهان از جمله هندوئیسم، بودیسم، جینیسم و سیک است و در طول تاریخ میزبان '
            'امپراتوری‌های موریه، گوپتا و مغول بوده؛ تاج محل در آگرا، که به دستور شاه‌جهان ساخته شد، یکی از '
            'شناخته‌شده‌ترین نمادهای معماری این دوران و جهان است.\n\n'
            'هند با بیش از ۱.۴ میلیارد نفر جمعیت، تنوع زبانی و فرهنگی خیره‌کننده‌ای دارد؛ صدها زبان و گویش در '
            'این کشور رایج است. دهلی‌نو پایتخت، و ممبی (بمبئی) مرکز اقتصادی و صنعت سینمای بالیوود این کشور به‌شمار '
            'می‌روند. اقتصاد هند یکی از سریع‌ترین اقتصادهای در حال رشد جهان در حوزه‌ی فناوری اطلاعات، خدمات و '
            'تولید است.'
        ),
        'en': (
            'India is the world\'s second most populous country and its largest democracy, located in South Asia '
            'and bordering Pakistan, China, Nepal, Bhutan, Bangladesh, and Myanmar. It has extraordinary '
            'geographic and climatic diversity, from the Himalayan peaks in the north to the Indian Ocean coast in '
            'the south.\n\n'
            'India is the birthplace of several of the world\'s major religions, including Hinduism, Buddhism, '
            'Jainism, and Sikhism, and has historically hosted the Maurya, Gupta, and Mughal empires; the Taj '
            'Mahal in Agra, built on the orders of Shah Jahan, is one of the most recognized architectural symbols '
            'of that era and of the world.\n\n'
            'With a population of over 1.4 billion, India has remarkable linguistic and cultural diversity, with '
            'hundreds of languages and dialects spoken across the country. New Delhi is the capital, and Mumbai '
            'is the country\'s economic hub and the home of the Bollywood film industry. India\'s economy is one '
            'of the fastest-growing in the world in information technology, services, and manufacturing.'
        ),
    },
}


def expand(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    for slug, texts in DESCRIPTIONS.items():
        Country.objects.filter(slug=slug).update(
            description=texts['fa'],
            description_fa=texts['fa'],
            description_en=texts['en'],
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_fix_image_urls'),
    ]

    operations = [
        migrations.RunPython(expand, noop),
    ]
