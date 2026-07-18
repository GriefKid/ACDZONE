from django.db import migrations
from django.utils.text import slugify

# Attractions for the remaining Asian/tourism-focus countries. Every
# filename here was confirmed to exist on Wikimedia Commons via WebSearch
# before being used (Special:FilePath redirect, no hash-path guessing).
# Where no single confirmed specific-landmark photo turned up in search,
# the filename is left as '' — an honest gap rather than a fabricated URL
# (same policy as migrations 0011 and 0015).
ATTRACTIONS = {
    'afghanistan': [
        ('مسجد کبود مزار شریف', 'The Blue Mosque of Mazar-i-Sharif',
         'یکی از باشکوه‌ترین اماکن مذهبی افغانستان با کاشی‌کاری‌های آبی خیره‌کننده.',
         'One of Afghanistan\'s most magnificent religious sites, famed for its dazzling blue tilework.',
         'Blue Mosque in Mazar-e-Sharif.jpg'),
    ],
    'bahrain': [
        ('قلعه‌ی بحرین', "Bahrain Fort (Qal'at al-Bahrain)",
         'اثری باستانی ثبت‌شده در یونسکو که پایتخت باستانی تمدن دیلمون بر آن بنا شده بود.',
         'A UNESCO-listed archaeological site, once the ancient capital of the Dilmun civilization.',
         ''),
        ('مسجد جامع الفاتح', 'Al Fateh Grand Mosque',
         'یکی از بزرگ‌ترین مساجد جهان با گنبدی از فایبرگلاس و ظرفیت هزاران نمازگزار.',
         'One of the largest mosques in the world, with a fiberglass dome and capacity for thousands of worshippers.',
         ''),
    ],
    'bangladesh': [
        ('قلعه‌ی لالباغ', 'Lalbagh Fort, Dhaka',
         'قلعه‌ای ناتمام از دوران مغول در قلب داکا با معماری تاریخی.',
         'An unfinished Mughal-era fort in the heart of Dhaka, with striking historic architecture.',
         "Lalbagh Fort, Dhaka, Bangladesh.jpg"),
        ('جنگل سوندربان', 'The Sundarbans',
         'بزرگ‌ترین جنگل مانگرو جهان و زیستگاه ببر بنگال، ثبت‌شده در یونسکو.',
         'The world\'s largest mangrove forest and home to the Bengal tiger, a UNESCO World Heritage Site.',
         ''),
    ],
    'bhutan': [
        ('صومعه‌ی تاکتسانگ (لانه‌ی ببر)', 'Paro Taktsang (Tiger\'s Nest)',
         'صومعه‌ای معلق بر صخره‌ای مرتفع در دره‌ی پارو، یکی از نمادی‌ترین مکان‌های بوتان.',
         'A monastery clinging to a high cliff in the Paro valley, one of Bhutan\'s most iconic sites.',
         'Paro Taktsang, Bhutan (edited).jpg'),
        ('دژونگ پوناخا', 'Punakha Dzong',
         'زیباترین دژونگ بوتان، در محل تلاقی دو رودخانه با معماری سنتی خیره‌کننده.',
         'Bhutan\'s most beautiful dzong, at the confluence of two rivers with stunning traditional architecture.',
         'Punakha Dzong BHUTAN.jpg'),
    ],
    'brunei': [
        ('مسجد سلطان عمر علی سیف‌الدین', 'Sultan Omar Ali Saifuddien Mosque',
         'مسجدی باشکوه با گنبد طلاکاری‌شده در کنار رودخانه‌ی برونئی.',
         'A magnificent mosque with a gold-leafed dome beside the Brunei River.',
         'Sultan Omar Ali Saifuddin Mosque (18564486326).jpg'),
        ('کامپونگ آیر', 'Kampong Ayer (Water Village)',
         'بزرگ‌ترین روستای روی آب جهان، با خانه‌های چوبی سنتی بر ستون‌ها.',
         'The world\'s largest stilt village, with traditional wooden houses built over the water.',
         ''),
    ],
    'cambodia': [
        ('معبد آنکوروات', 'Angkor Wat',
         'بزرگ‌ترین بنای مذهبی جهان و نماد اصلی کامبوج، از میراث امپراتوری خمر.',
         'The largest religious monument in the world and Cambodia\'s foremost symbol, a legacy of the Khmer Empire.',
         'Angkor Wat.jpg'),
        ('معبد بایون', 'Bayon Temple',
         'معبدی معروف به چهره‌های سنگی عظیم در قلب آنکور تُم.',
         'A temple famous for its giant carved stone faces, in the heart of Angkor Thom.',
         'Bayon temple at Angkor Thom 01.jpg'),
    ],
    'kazakhstan': [
        ('برج بایترک', 'Bayterek Tower, Astana',
         'نماد معماری پایتخت قزاقستان با چشم‌اندازی پانورامیک از شهر.',
         'An architectural symbol of the Kazakh capital, offering a panoramic view of the city.',
         ''),
        ('دره‌ی چارین', 'Charyn Canyon',
         'دره‌ای صخره‌ای خیره‌کننده که گاه با گرند کنیون آمریکا مقایسه می‌شود.',
         'A stunning canyon sometimes compared to the Grand Canyon in the United States.',
         'Charyn Canyon, Kazakhstan 02.jpg'),
    ],
    'kuwait': [
        ('برج‌های کویت', 'Kuwait Towers',
         'نماد معماری کویت با سه برج مخروطی‌شکل بر ساحل خلیج فارس.',
         'Kuwait\'s architectural icon, three cone-shaped towers on the Gulf shoreline.',
         'Kuwait towers.jpg'),
        ('مسجد جامع کویت', 'Grand Mosque, Kuwait City',
         'بزرگ‌ترین مسجد کویت با معماری اسلامی سنتی و گنجایش هزاران نمازگزار.',
         'Kuwait\'s largest mosque, with traditional Islamic architecture and capacity for thousands.',
         'Grand mosque, Kuwait 1.jpg'),
    ],
    'kyrgyzstan': [
        ('دریاچه‌ی ایسیک‌کول', 'Issyk-Kul Lake',
         'دومین دریاچه‌ی آب‌شور بزرگ جهان، در دل کوه‌های تیان‌شان.',
         'The world\'s second-largest saline lake, nestled in the Tian Shan mountains.',
         ''),
        ('پارک ملی آلا-آرچا', 'Ala-Archa National Park',
         'پارکی کوهستانی نزدیک بیشکک، مقصدی محبوب برای کوه‌نوردی و طبیعت‌گردی.',
         'A mountain park near Bishkek, a popular destination for hiking and nature tourism.',
         ''),
    ],
    'laos': [
        ('استوپای طلایی پاتات لوانگ', 'Pha That Luang, Vientiane',
         'استوپای طلاکاری‌شده و نماد ملی لائوس در پایتخت این کشور.',
         'A gold-covered Buddhist stupa and national symbol of Laos, in the capital Vientiane.',
         ''),
        ('شهر باستانی لوانگ‌پرابانگ', 'Luang Prabang',
         'پایتخت باستانی لائوس با معابد طلاکاری‌شده، ثبت‌شده در یونسکو.',
         'Laos\'s ancient royal capital, with gold-leafed temples, a UNESCO World Heritage Site.',
         ''),
    ],
    'mongolia': [
        ('مجسمه‌ی سوارکار چنگیزخان', 'Genghis Khan Equestrian Statue',
         'بلندترین مجسمه‌ی سوارکار جهان، در نزدیکی اولان‌باتور.',
         'The world\'s tallest equestrian statue, near Ulaanbaatar.',
         'Chinggis Khaan statue Complex.jpg'),
        ('کویر گبی', 'The Gobi Desert',
         'یکی از بزرگ‌ترین کویرهای جهان با کوه‌های شنی و کشفیات فسیلی دایناسور.',
         'One of the world\'s largest deserts, with sand dunes and famous dinosaur fossil discoveries.',
         ''),
    ],
    'myanmar': [
        ('پاگودای شوداگون', 'Shwedagon Pagoda',
         'استوپای طلایی و مقدس‌ترین مکان بودایی میانمار در یانگون.',
         'A golden stupa and the holiest Buddhist site in Myanmar, in Yangon.',
         'Shwedagon pagoda.jpg'),
        ('معابد باگان', 'Bagan Temples',
         'دشتی با هزاران معبد و استوپای باستانی از قرن نهم تا سیزدهم میلادی.',
         'A plain scattered with thousands of ancient temples and stupas from the 9th to 13th centuries.',
         ''),
    ],
    'nepal': [
        ('معبد پاشوپاتی‌ناث', 'Pashupatinath Temple, Kathmandu',
         'یکی از مقدس‌ترین معابد هندو جهان، ثبت‌شده در یونسکو.',
         'One of the holiest Hindu temples in the world, a UNESCO World Heritage Site.',
         'Pashupatinath Temple, Kathmandu.jpg'),
        ('اردوگاه پایه‌ی اورست', 'Everest Base Camp',
         'مقصد نهایی بسیاری از کوه‌نوردان جهان در دامنه‌ی بلندترین قله‌ی زمین.',
         'The ultimate destination for many of the world\'s trekkers, at the foot of the world\'s tallest peak.',
         ''),
    ],
    'oman': [
        ('مسجد جامع سلطان قابوس', 'Sultan Qaboos Grand Mosque',
         'بزرگ‌ترین مسجد عمان با فرشی دست‌باف عظیم و لوستری خیره‌کننده.',
         "Oman's largest mosque, with a huge hand-woven carpet and a spectacular chandelier.",
         ''),
        ('قلعه‌ی نزوا', 'Nizwa Fort',
         'یکی از معروف‌ترین قلعه‌های عمان با برج مدور عظیم.',
         "One of Oman's most famous forts, with a massive round tower.",
         ''),
    ],
    'palestine': [
        ('کلیسای میلاد بیت‌لحم', 'Church of the Nativity, Bethlehem',
         'یکی از کهن‌ترین کلیساهای جهان که بر محل تولد عیسی مسیح بنا شده، ثبت‌شده در یونسکو.',
         'One of the world\'s oldest churches, built over the traditional birthplace of Jesus Christ, a UNESCO site.',
         'Bethlehem Church of the Nativity interior.jpg'),
        ('گنبد الصخره', 'Dome of the Rock, Jerusalem',
         'یکی از قدیمی‌ترین و مقدس‌ترین بناهای اسلامی جهان.',
         'One of the oldest and holiest structures in Islamic history.',
         ''),
    ],
    'philippines': [
        ('تپه‌های شکلاتی بوهول', 'Chocolate Hills, Bohol',
         'بیش از هزار تپه‌ی مخروطی‌شکل که در فصل خشک به رنگ قهوه‌ای درمی‌آیند.',
         'Over a thousand cone-shaped hills that turn brown in the dry season.',
         'Chocolate Hills.jpg'),
        ('تراس‌های برنج بانائوه', 'Banaue Rice Terraces',
         'تراس‌های برنج دوهزارساله که توسط اقوام بومی بر دامنه‌ی کوه‌ها تراشیده شده‌اند.',
         'Two-thousand-year-old rice terraces carved into the mountainside by indigenous peoples.',
         'Banaue Rice Terraces, Philippines.jpg'),
    ],
    'russia': [
        ("کلیسای جامع سنت باسیل", "Saint Basil's Cathedral, Moscow",
         'کلیسایی رنگارنگ و افسانه‌ای در میدان سرخ مسکو، نماد شناخته‌شده‌ی روسیه.',
         "A colorful, legendary cathedral on Red Square, one of Russia's most recognizable symbols.",
         "Saint Basil's Cathedral in Moscow.jpg"),
        ('موزه‌ی ارمیتاژ', 'The Hermitage Museum, Saint Petersburg',
         'یکی از بزرگ‌ترین و کهن‌ترین موزه‌های هنری جهان در کاخ زمستانی سابق تزارها.',
         "One of the world's largest and oldest art museums, in the former Winter Palace of the Tsars.",
         ''),
    ],
    'singapore': [
        ('مارینا بی‌ساندز', 'Marina Bay Sands',
         'مجتمعی نمادین با استخر بی‌کران روی پشت‌بام و چشم‌اندازی به اسکای‌لاین سنگاپور.',
         "An iconic complex with a rooftop infinity pool overlooking Singapore's skyline.",
         'Gardens by the Bay and Marina Bay Sands, Singapore, at dusk - 20120928.jpg'),
        ('باغ‌های خلیج', 'Gardens by the Bay',
         'باغی آینده‌نگرانه با درختان مصنوعی غول‌پیکر موسوم به سوپرتری.',
         'A futuristic garden with giant artificial trees known as Supertrees.',
         'Gardens by the Bay South viewed from Sands Sky Park, Marina Bay Sands Hotel, Singapore.jpg'),
    ],
    'sri-lanka': [
        ('صخره‌ی سیگیریا', 'Sigiriya Rock Fortress',
         'دژی باستانی بر صخره‌ای عظیم با نقاشی‌های دیواری معروف، ثبت‌شده در یونسکو.',
         'An ancient rock fortress famed for its wall paintings, a UNESCO World Heritage Site.',
         'Sigiriya Sri Lanka.jpg'),
        ('معبد دندان مقدس کندی', 'Temple of the Sacred Tooth Relic, Kandy',
         'مقدس‌ترین معبد بودایی سری‌لانکا، محل نگهداری دندان مقدس بودا.',
         "Sri Lanka's holiest Buddhist temple, said to house a relic of the Buddha's tooth.",
         'Sri Lanka - 029 - Kandy Temple of the Tooth.jpg'),
    ],
    'tajikistan': [
        ('دریاچه‌ی اسکندرکول', 'Iskanderkul Lake',
         'دریاچه‌ای یخچالی زیبا در دل کوه‌های فان، محبوب برای طبیعت‌گردی.',
         'A beautiful glacial lake in the Fann Mountains, popular for nature tourism.',
         'Iskander-kul, Tajikistan.JPG'),
        ('شاهراه پامیر', 'The Pamir Highway',
         'یکی از مرتفع‌ترین و خیره‌کننده‌ترین شاهراه‌های جهان که از دل کوه‌های پامیر می‌گذرد.',
         "One of the world's highest and most spectacular highways, cutting through the Pamir Mountains.",
         ''),
    ],
    'turkmenistan': [
        ('دروازه‌ی جهنم', 'Darvaza Gas Crater ("Door to Hell")',
         'حفره‌ای گازی که دهه‌هاست در دل کویر قره‌قوم می‌سوزد.',
         "A gas crater that has been burning for decades in the heart of the Karakum Desert.",
         'Darvasa gas crater panorama.jpg'),
        ('ساختمان‌های مرمرین عشق‌آباد', 'Ashgabat\'s White Marble Buildings',
         'پایتختی با بیشترین تراکم ساختمان‌های پوشیده از مرمر سفید در جهان.',
         "A capital city holding the world record for the highest concentration of white marble-clad buildings.",
         ''),
    ],
    'uzbekistan': [
        ('میدان رجستان سمرقند', 'Registan Square, Samarkand',
         'میدانی باشکوه با سه مدرسه‌ی کاشی‌کاری‌شده، شاهکار معماری تیموری.',
         'A magnificent square with three tiled madrasas, a masterpiece of Timurid architecture.',
         'Registan Samarkand Uzbekistan.JPG'),
        ('شهر باستانی بخارا', 'Historic Centre of Bukhara',
         'شهری با بیش از هزار سال تاریخ در مسیر جاده‌ی ابریشم، ثبت‌شده در یونسکو.',
         'A city with over a thousand years of history on the Silk Road, a UNESCO World Heritage Site.',
         ''),
    ],
    'armenia': [
        ('صومعه‌ی گقارد', 'Geghard Monastery',
         'صومعه‌ای قرون‌وسطایی که بخشی از آن در دل صخره تراشیده شده، ثبت‌شده در یونسکو.',
         'A medieval monastery partly carved into the surrounding cliff, a UNESCO World Heritage Site.',
         'Geghard gavit-IMG 2564.JPG'),
        ('دریاچه‌ی سوان', 'Lake Sevan',
         'بزرگ‌ترین دریاچه‌ی قفقاز و ارمنستان، مقصدی محبوب برای تابستان.',
         "The largest lake in the Caucasus and in Armenia, a popular summer destination.",
         ''),
    ],
    'azerbaijan': [
        ('برج‌های شعله باکو', 'Flame Towers, Baku',
         'سه برج شعله‌مانند و نماد مدرن باکو، پایتخت آذربایجان.',
         "Three flame-shaped skyscrapers, a modern symbol of Baku, Azerbaijan's capital.",
         ''),
        ('ذخیره‌گاه گوبوستان', 'Gobustan Rock Art Cultural Landscape',
         'ذخیره‌گاهی با هزاران نقش سنگی باستانی، ثبت‌شده در یونسکو.',
         'A reserve with thousands of ancient petroglyphs, a UNESCO World Heritage Site.',
         ''),
    ],
    'cyprus': [
        ('مقبره‌های پادشاهان پافوس', 'Tombs of the Kings, Paphos',
         'مجموعه‌ای باستانی از مقابر تراشیده در صخره، ثبت‌شده در یونسکو.',
         'An ancient necropolis of tombs carved into rock, a UNESCO World Heritage Site.',
         'Tombs of the Kings Paphos Cyprus 23.jpg'),
        ('کوریون باستانی', 'Ancient Kourion',
         'شهر باستانی یونانی-رومی با آمفی‌تئاتری خیره‌کننده مشرف به دریای مدیترانه.',
         'An ancient Greco-Roman city with a stunning amphitheater overlooking the Mediterranean.',
         'Ancient Kourion, Episkopi, Cyprus - panoramio (3).jpg'),
    ],
    'georgia': [
        ('برج‌های سوانتی', 'Svaneti Towers, Ushguli',
         'برج‌های سنگی قرون‌وسطایی در روستاهای مرتفع سوانتی، ثبت‌شده در یونسکو.',
         'Medieval stone towers in the high villages of Svaneti, a UNESCO World Heritage Site.',
         'Ushguli Svaneti Georgia.JPG'),
        ('قلعه‌ی ناریکالا', 'Narikala Fortress, Tbilisi',
         'دژی باستانی مشرف به تفلیس و رودخانه‌ی مت‌کواری.',
         'An ancient fortress overlooking Tbilisi and the Mtkvari River.',
         ''),
    ],
    'iraq': [
        ('زیگورات اور', 'The Great Ziggurat of Ur',
         'یکی از بهترین‌حفظ‌شده‌ترین زیگورات‌های بین‌النهرین باستان.',
         'One of the best-preserved ziggurats of ancient Mesopotamia.',
         'Ziggurat of Ur Iraq.jpg'),
        ('منارهٔ ملویه سامرا', 'Malwiya Minaret, Samarra',
         'مناره‌ای مارپیچی و منحصربه‌فرد از مسجد بزرگ سامرا، ثبت‌شده در یونسکو.',
         'A unique spiral minaret of the Great Mosque of Samarra, a UNESCO World Heritage Site.',
         ''),
    ],
    'israel': [
        ('دیوار غربی اورشلیم', 'The Western Wall, Jerusalem',
         'مقدس‌ترین مکان یهودیت برای دعا، بازمانده از دیوار معبد دوم.',
         "Judaism's holiest place of prayer, a remnant of the Second Temple's retaining wall.",
         'The Western Wall.jpg'),
        ('دژ مسادا', 'Masada',
         'قلعه‌ای باستانی بر فراز صخره‌ای مشرف به دریای مرده، ثبت‌شده در یونسکو.',
         'An ancient fortress atop a rock plateau overlooking the Dead Sea, a UNESCO World Heritage Site.',
         ''),
    ],
    'lebanon': [
        ('معابد بعلبک', 'Baalbek Roman Temples',
         'یکی از عظیم‌ترین مجموعه‌های معابد رومی جهان در دره‌ی بقاع، ثبت‌شده در یونسکو.',
         "One of the world's largest Roman temple complexes, in the Beqaa Valley, a UNESCO World Heritage Site.",
         'Baalbek, Lebanon.JPG'),
        ('غار جعیتا', 'Jeita Grotto',
         'مجموعه‌ای از غارهای آهکی خیره‌کننده در نزدیکی بیروت.',
         'A stunning system of limestone caves near Beirut.',
         ''),
    ],
    'maldives': [
        ('ویلاهای روی آب مالدیو', 'Maldives Overwater Villas',
         'استراحتگاه‌های لوکس با ویلاهای روی آب و دسترسی مستقیم به آب‌های فیروزه‌ای.',
         'Luxury resorts with overwater villas and direct access to turquoise waters.',
         'The Residence MALDIVES water villas.jpg'),
    ],
    'north-korea': [
        ('برج جوچه', 'Juche Tower, Pyongyang',
         'برجی یادبود در ساحل رودخانه‌ی تدونگ، نمادی از پایتخت کره‌ی شمالی.',
         "A monument tower on the bank of the Taedong River, a symbol of North Korea's capital.",
         'Juche Tower, Pyongyang, North Korea (25 September 2008).jpg'),
        ('کوه پکتو', 'Mount Paektu',
         'بلندترین کوه شبه‌جزیره‌ی کره و مکانی با اهمیت اسطوره‌ای برای مردم کره.',
         'The tallest mountain on the Korean Peninsula, with deep mythological significance.',
         ''),
    ],
    'syria': [
        ('مسجد جامع اموی دمشق', 'Umayyad Mosque, Damascus',
         'یکی از کهن‌ترین و مقدس‌ترین مساجد جهان اسلام، ثبت‌شده در یونسکو.',
         'One of the oldest and holiest mosques in the Islamic world, a UNESCO World Heritage Site.',
         'Umayyad Mosque, Damascus, Syria.JPG'),
        ('شهر باستانی پالمیرا', 'Palmyra',
         'شهری باستانی کاروان‌سالار در دل کویر سوریه، ثبت‌شده در یونسکو.',
         "An ancient caravan city in the Syrian desert, a UNESCO World Heritage Site.",
         'Palmyra, Syria - 2.jpg'),
    ],
    'taiwan': [
        ('برج تایپه ۱۰۱', 'Taipei 101',
         'زمانی بلندترین ساختمان جهان و نماد اصلی تایپه.',
         "Once the world's tallest building and Taipei's foremost landmark.",
         'Taipei Taiwan Taipei-101-Tower-01.jpg'),
        ('موزه‌ی کاخ ملی', 'National Palace Museum, Taipei',
         'یکی از بزرگ‌ترین مجموعه‌های هنر و آثار باستانی چین در جهان.',
         "One of the world's largest collections of Chinese art and artifacts.",
         'NationalPalace MuseumFrontView.jpg'),
    ],
    'timor-leste': [
        ('مجسمه‌ی کریستو ری', 'Cristo Rei of Dili',
         'مجسمه‌ای عظیم از عیسی مسیح بر فراز دماغه‌ی فاتوکاما با چشم‌اندازی به اقیانوس.',
         'A colossal statue of Jesus Christ atop Cape Fatucama, overlooking the ocean.',
         'Cristo Rei Dili Timor Leste.jpg'),
        ('جزیره‌ی آتائورو', 'Atauro Island',
         'جزیره‌ای با آب‌های بکر و صخره‌های مرجانی، مقصدی نوظهور برای غواصی.',
         'An island with pristine waters and coral reefs, an emerging diving destination.',
         ''),
    ],
    'yemen': [
        ('شهر باستانی صنعا', 'Old City of Sana\'a',
         'شهری با خانه‌های برجی خشتی چندطبقه، ثبت‌شده در یونسکو.',
         'A city of multi-story mudbrick tower houses, a UNESCO World Heritage Site.',
         "Old City of Sana'a-111110.jpg"),
        ('جزیره‌ی سقطری', 'Socotra Island',
         'جزیره‌ای منزوی با گیاهان و جانوران بومی منحصربه‌فرد از جمله درخت خون‌اژدها.',
         'An isolated island with unique endemic flora and fauna, including the dragon\'s blood tree.',
         ''),
    ],
}

# One real, well-known hotel per country. Photos were not individually
# WebSearch-verified for this batch given the volume — rather than guess
# URLs, every image_url here is left blank so the site shows the graceful
# icon fallback instead of a broken/fabricated image (same honest-gap
# approach used for hotels without confirmed photos in migration 0015).
HOTELS = {
    'afghanistan': ('کابل سرینا هتل', 'Kabul Serena Hotel', 'کابل', 'Kabul', 5),
    'bahrain': ('ریتز-کارلتون بحرین', 'The Ritz-Carlton, Bahrain', 'منامه', 'Manama', 5),
    'bangladesh': ('پن پاسیفیک سونارگائون داکا', 'Pan Pacific Sonargaon Dhaka', 'داکا', 'Dhaka', 5),
    'bhutan': ('تاج تاشی', 'Taj Tashi', 'تیمفو', 'Thimphu', 5),
    'brunei': ('امپایر برونئی', 'The Empire Brunei', 'بندر سری‌بگاوان', 'Bandar Seri Begawan', 5),
    'cambodia': ('رافلز لو رویال', 'Raffles Hotel Le Royal', 'پنوم‌پن', 'Phnom Penh', 5),
    'kazakhstan': ('ریکسوس پرزیدنت آستانه', 'Rixos President Astana', 'آستانه', 'Astana', 5),
    'kuwait': ('فور سیزنز هتل کویت', 'Four Seasons Hotel Kuwait', 'شهر کویت', 'Kuwait City', 5),
    'kyrgyzstan': ('هایت ریجنسی بیشکک', 'Hyatt Regency Bishkek', 'بیشکک', 'Bishkek', 5),
    'laos': ('هتل سته‌ی پالاس', 'Settha Palace Hotel', 'ویانتیان', 'Vientiane', 4),
    'mongolia': ('شانگری-لا اولان‌باتور', 'Shangri-La Hotel Ulaanbaatar', 'اولان‌باتور', 'Ulaanbaatar', 5),
    'myanmar': ('هتل استرند', 'The Strand Hotel', 'یانگون', 'Yangon', 5),
    'nepal': ('دواریکاز هتل', "Dwarika's Hotel", 'کاتماندو', 'Kathmandu', 5),
    'oman': ('البستان پالاس', 'Al Bustan Palace, a Ritz-Carlton Hotel', 'مسقط', 'Muscat', 5),
    'palestine': ('جاسر پالاس هتل', 'Jacir Palace Hotel', 'بیت‌لحم', 'Bethlehem', 5),
    'philippines': ('منیل هتل', 'The Manila Hotel', 'مانیل', 'Manila', 5),
    'russia': ('هتل نشنال مسکو', 'Hotel National Moscow', 'مسکو', 'Moscow', 5),
    'singapore': ('رافلز سنگاپور', 'Raffles Hotel Singapore', 'سنگاپور', 'Singapore', 5),
    'sri-lanka': ('گال فیس هتل', 'Galle Face Hotel', 'کلمبو', 'Colombo', 5),
    'tajikistan': ('هایت ریجنسی دوشنبه', 'Hyatt Regency Dushanbe', 'دوشنبه', 'Dushanbe', 5),
    'turkmenistan': ('سوفیتل اوغوزکنت', 'Sofitel Oguzkent', 'عشق‌آباد', 'Ashgabat', 5),
    'uzbekistan': ('هتل ازبکستان', 'Hotel Uzbekistan', 'تاشکند', 'Tashkent', 4),
    'armenia': ('ارمنستان ماریوت ایروان', 'Armenia Marriott Hotel Yerevan', 'ایروان', 'Yerevan', 5),
    'azerbaijan': ('فور سیزنز باکو', 'Four Seasons Hotel Baku', 'باکو', 'Baku', 5),
    'cyprus': ('فور سیزنز لیماسول', 'Four Seasons Hotel Limassol', 'لیماسول', 'Limassol', 5),
    'georgia': ('رومز هتل تفلیس', 'Rooms Hotel Tbilisi', 'تفلیس', 'Tbilisi', 4),
    'iraq': ('بغداد هتل', 'Baghdad Hotel', 'بغداد', 'Baghdad', 4),
    'israel': ('کینگ دیوید هتل', 'King David Hotel Jerusalem', 'اورشلیم', 'Jerusalem', 5),
    'lebanon': ('فینیشیا هتل بیروت', 'Phoenicia Hotel Beirut', 'بیروت', 'Beirut', 5),
    'maldives': ('سونوا فوشی', 'Soneva Fushi', 'باآ آتول', 'Baa Atoll', 5),
    'north-korea': ('یانگاکدو اینترنشنال هتل', 'Yanggakdo International Hotel', 'پیونگ‌یانگ', 'Pyongyang', 4),
    'syria': ('فور سیزنز دمشق', 'Four Seasons Hotel Damascus', 'دمشق', 'Damascus', 5),
    'taiwan': ('گرند هتل تایپه', 'The Grand Hotel Taipei', 'تایپه', 'Taipei', 5),
    'timor-leste': ('تیمور پلازا هتل', 'Timor Plaza Hotel', 'دیلی', 'Dili', 4),
    'yemen': ('موونپیک هتل صنعا', "Mövenpick Hotel Sana'a", 'صنعا', "Sana'a", 5),
}


def commons_url(filename):
    from urllib.parse import quote
    return 'https://commons.wikimedia.org/wiki/Special:FilePath/' + quote(filename.replace(' ', '_'))


def seed(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    Attraction = apps.get_model('core', 'Attraction')
    Hotel = apps.get_model('core', 'Hotel')

    for slug, items in ATTRACTIONS.items():
        country = Country.objects.filter(slug=slug).first()
        if not country:
            continue
        for order, (name_fa, name_en, summary_fa, summary_en, filename) in enumerate(items):
            if Attraction.objects.filter(country=country, name_en=name_en).exists():
                continue
            base_slug = slugify(name_en, allow_unicode=True) or 'attraction'
            slug_val = base_slug
            n = 1
            while Attraction.objects.filter(country=country, slug=slug_val).exists():
                n += 1
                slug_val = f'{base_slug}-{n}'
            Attraction.objects.create(
                country=country,
                name=name_fa, name_fa=name_fa, name_en=name_en,
                slug=slug_val,
                summary=summary_fa, summary_fa=summary_fa, summary_en=summary_en,
                description=summary_fa, description_fa=summary_fa, description_en=summary_en,
                image_url=commons_url(filename) if filename else '',
                is_active=True, order=order,
            )

    for slug, (name_fa, name_en, city_fa, city_en, stars) in HOTELS.items():
        country = Country.objects.filter(slug=slug).first()
        if not country:
            continue
        if Hotel.objects.filter(country=country, name_en=name_en).exists():
            continue
        summary_fa = f'یکی از شناخته‌شده‌ترین هتل‌های {country.name_fa or country.name}.'
        summary_en = f'One of the best-known hotels in {country.name_en or name_en}.'
        Hotel.objects.create(
            country=country,
            name=name_fa, name_fa=name_fa, name_en=name_en,
            city=city_fa, city_fa=city_fa, city_en=city_en,
            star_rating=stars,
            summary=summary_fa, summary_fa=summary_fa, summary_en=summary_en,
            description=summary_fa, description_fa=summary_fa, description_en=summary_en,
            image_url='',
            is_active=True, order=0,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_expand_attractions_hotels_routes'),
    ]

    operations = [
        migrations.RunPython(seed, noop),
    ]
