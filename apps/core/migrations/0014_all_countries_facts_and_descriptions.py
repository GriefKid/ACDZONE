from django.db import migrations

# Quick facts (capital/official language/currency/calling code/best time to
# visit) for ALL 50 countries currently in the table — cheap, stable facts
# that don't need a photo, and immediately make every single country page
# richer, not just the 8 already touched.
FACTS = {
    'afghanistan': ('کابل', 'دری و پشتو', 'افغانی', '+93', 'آوریل تا ژوئن و سپتامبر تا اکتبر'),
    'bahrain': ('منامه', 'عربی', 'دینار بحرین', '+973', 'نوامبر تا مارس'),
    'bangladesh': ('داکا', 'بنگالی', 'تاکای بنگلادش', '+880', 'نوامبر تا فوریه'),
    'bhutan': ('تیمفو', 'دزونگ‌خا', 'نگولتروم بوتان', '+975', 'مارس تا مه و سپتامبر تا نوامبر'),
    'brunei': ('بندر سری‌بگاوان', 'مالایی', 'دلار برونئی', '+673', 'مارس تا آوریل'),
    'cambodia': ('پنوم‌پن', 'خمر', 'ریل کامبوج', '+855', 'نوامبر تا مارس'),
    'china': ('پکن', 'ماندارین چینی', 'یوان چین (رنمینبی)', '+86', 'سپتامبر تا نوامبر و مارس تا مه'),
    'india': ('دهلی نو', 'هندی و انگلیسی', 'روپیه هند', '+91', 'اکتبر تا مارس'),
    'indonesia': ('جاکارتا', 'اندونزیایی', 'روپیه اندونزی', '+62', 'مه تا سپتامبر'),
    'iran': ('تهران', 'فارسی', 'ریال ایران', '+98', 'آوریل تا مه و سپتامبر تا اکتبر'),
    'japan': ('توکیو', 'ژاپنی', 'ین ژاپن', '+81', 'مارس تا مه و سپتامبر تا نوامبر'),
    'jordan': ('امان', 'عربی', 'دینار اردن', '+962', 'مارس تا مه و سپتامبر تا نوامبر'),
    'kazakhstan': ('آستانه', 'قزاقی و روسی', 'تنگه قزاقستان', '+7', 'مه تا سپتامبر'),
    'kuwait': ('شهر کویت', 'عربی', 'دینار کویت', '+965', 'نوامبر تا مارس'),
    'kyrgyzstan': ('بیشکک', 'قرقیزی و روسی', 'سام قرقیزستان', '+996', 'ژوئن تا سپتامبر'),
    'laos': ('ویانتیان', 'لائو', 'کیپ لائوس', '+856', 'نوامبر تا فوریه'),
    'malaysia': ('کوالالامپور', 'مالایی', 'رینگیت مالزی', '+60', 'دسامبر تا فوریه'),
    'mongolia': ('اولان‌باتور', 'مغولی', 'توگروگ مغولستان', '+976', 'ژوئن تا سپتامبر'),
    'myanmar': ('نای‌پی‌داو', 'برمه‌ای', 'کیات میانمار', '+95', 'نوامبر تا فوریه'),
    'nepal': ('کاتماندو', 'نپالی', 'روپیه نپال', '+977', 'سپتامبر تا نوامبر و مارس تا مه'),
    'oman': ('مسقط', 'عربی', 'ریال عمان', '+968', 'اکتبر تا آوریل'),
    'pakistan': ('اسلام‌آباد', 'اردو و انگلیسی', 'روپیه پاکستان', '+92', 'اکتبر تا آوریل'),
    'palestine': ('رام‌الله', 'عربی', 'دینار اردن و شِکل اسرائیل', '+970', 'مارس تا مه و سپتامبر تا نوامبر'),
    'philippines': ('مانیل', 'فیلیپینی و انگلیسی', 'پزوی فیلیپین', '+63', 'دسامبر تا فوریه'),
    'qatar': ('دوحه', 'عربی', 'ریال قطر', '+974', 'نوامبر تا مارس'),
    'russia': ('مسکو', 'روسی', 'روبل روسیه', '+7', 'مه تا سپتامبر'),
    'saudi-arabia': ('ریاض', 'عربی', 'ریال سعودی', '+966', 'نوامبر تا مارس'),
    'singapore': ('سنگاپور', 'انگلیسی، مالایی، ماندارین و تامیل', 'دلار سنگاپور', '+65', 'فوریه تا آوریل'),
    'south-korea': ('سئول', 'کره‌ای', 'وون کره جنوبی', '+82', 'مارس تا مه و سپتامبر تا نوامبر'),
    'sri-lanka': ('کلمبو (سری جایاواردنه‌پورا کوته، پایتخت اداری)', 'سینهالی و تامیل', 'روپیه سریلانکا', '+94', 'دسامبر تا مارس'),
    'tajikistan': ('دوشنبه', 'تاجیکی', 'سامانی تاجیکستان', '+992', 'مه تا سپتامبر'),
    'thailand': ('بانکوک', 'تایلندی', 'بات تایلند', '+66', 'نوامبر تا فوریه'),
    'turkey': ('آنکارا', 'ترکی', 'لیر ترکیه', '+90', 'آوریل تا ژوئن و سپتامبر تا نوامبر'),
    'united-arab-emirates': ('ابوظبی', 'عربی', 'درهم امارات', '+971', 'نوامبر تا مارس'),
    'uzbekistan': ('تاشکند', 'ازبکی', 'سام ازبکستان', '+998', 'مارس تا مه و سپتامبر تا نوامبر'),
    'vietnam': ('هانوی', 'ویتنامی', 'دونگ ویتنام', '+84', 'نوامبر تا آوریل'),
    'armenia': ('ایروان', 'ارمنی', 'درام ارمنستان', '+374', 'مه تا ژوئن و سپتامبر تا اکتبر'),
    'azerbaijan': ('باکو', 'آذربایجانی', 'مانات آذربایجان', '+994', 'آوریل تا ژوئن و سپتامبر تا اکتبر'),
    'cyprus': ('نیکوزیا', 'یونانی و ترکی', 'یورو', '+357', 'آوریل تا ژوئن و سپتامبر تا اکتبر'),
    'georgia': ('تفلیس', 'گرجی', 'لاری گرجستان', '+995', 'مه تا ژوئن و سپتامبر تا اکتبر'),
    'iraq': ('بغداد', 'عربی و کردی', 'دینار عراق', '+964', 'مارس تا مه و اکتبر تا نوامبر'),
    'israel': ('اورشلیم (بیت‌المقدس)', 'عبری و عربی', 'شِکل جدید اسرائیل', '+972', 'مارس تا مه و سپتامبر تا نوامبر'),
    'lebanon': ('بیروت', 'عربی', 'لیر لبنان', '+961', 'آوریل تا ژوئن و سپتامبر تا اکتبر'),
    'maldives': ('ماله', 'دیوهی', 'روفیه مالدیو', '+960', 'نوامبر تا آوریل'),
    'north-korea': ('پیونگ‌یانگ', 'کره‌ای', 'وون کره شمالی', '+850', 'آوریل تا ژوئن و سپتامبر تا اکتبر'),
    'syria': ('دمشق', 'عربی', 'لیر سوریه', '+963', 'مارس تا مه و سپتامبر تا نوامبر'),
    'taiwan': ('تایپه', 'ماندارین چینی', 'دلار جدید تایوان', '+886', 'اکتبر تا دسامبر'),
    'timor-leste': ('دیلی', 'تتوم و پرتغالی', 'دلار آمریکا', '+670', 'مه تا نوامبر'),
    'turkmenistan': ('عشق‌آباد', 'ترکمنی', 'مانات ترکمنستان', '+993', 'آوریل تا ژوئن و سپتامبر تا اکتبر'),
    'yemen': ('صنعا', 'عربی', 'ریال یمن', '+967', 'اکتبر تا فوریه'),
}

FACTS_EN = {
    'afghanistan': ('Kabul', 'Dari and Pashto', 'Afghan Afghani', '+93', 'April-June and September-October'),
    'bahrain': ('Manama', 'Arabic', 'Bahraini Dinar', '+973', 'November-March'),
    'bangladesh': ('Dhaka', 'Bengali', 'Bangladeshi Taka', '+880', 'November-February'),
    'bhutan': ('Thimphu', 'Dzongkha', 'Bhutanese Ngultrum', '+975', 'March-May and September-November'),
    'brunei': ('Bandar Seri Begawan', 'Malay', 'Brunei Dollar', '+673', 'March-April'),
    'cambodia': ('Phnom Penh', 'Khmer', 'Cambodian Riel', '+855', 'November-March'),
    'china': ('Beijing', 'Mandarin Chinese', 'Chinese Yuan (Renminbi)', '+86', 'September-November and March-May'),
    'india': ('New Delhi', 'Hindi and English', 'Indian Rupee', '+91', 'October-March'),
    'indonesia': ('Jakarta', 'Indonesian', 'Indonesian Rupiah', '+62', 'May-September'),
    'iran': ('Tehran', 'Persian', 'Iranian Rial', '+98', 'April-May and September-October'),
    'japan': ('Tokyo', 'Japanese', 'Japanese Yen', '+81', 'March-May and September-November'),
    'jordan': ('Amman', 'Arabic', 'Jordanian Dinar', '+962', 'March-May and September-November'),
    'kazakhstan': ('Astana', 'Kazakh and Russian', 'Kazakhstani Tenge', '+7', 'May-September'),
    'kuwait': ('Kuwait City', 'Arabic', 'Kuwaiti Dinar', '+965', 'November-March'),
    'kyrgyzstan': ('Bishkek', 'Kyrgyz and Russian', 'Kyrgyzstani Som', '+996', 'June-September'),
    'laos': ('Vientiane', 'Lao', 'Lao Kip', '+856', 'November-February'),
    'malaysia': ('Kuala Lumpur', 'Malay', 'Malaysian Ringgit', '+60', 'December-February'),
    'mongolia': ('Ulaanbaatar', 'Mongolian', 'Mongolian Tögrög', '+976', 'June-September'),
    'myanmar': ('Naypyidaw', 'Burmese', 'Myanmar Kyat', '+95', 'November-February'),
    'nepal': ('Kathmandu', 'Nepali', 'Nepalese Rupee', '+977', 'September-November and March-May'),
    'oman': ('Muscat', 'Arabic', 'Omani Rial', '+968', 'October-April'),
    'pakistan': ('Islamabad', 'Urdu and English', 'Pakistani Rupee', '+92', 'October-April'),
    'palestine': ('Ramallah', 'Arabic', 'Jordanian Dinar and Israeli Shekel', '+970', 'March-May and September-November'),
    'philippines': ('Manila', 'Filipino and English', 'Philippine Peso', '+63', 'December-February'),
    'qatar': ('Doha', 'Arabic', 'Qatari Riyal', '+974', 'November-March'),
    'russia': ('Moscow', 'Russian', 'Russian Ruble', '+7', 'May-September'),
    'saudi-arabia': ('Riyadh', 'Arabic', 'Saudi Riyal', '+966', 'November-March'),
    'singapore': ('Singapore', 'English, Malay, Mandarin, and Tamil', 'Singapore Dollar', '+65', 'February-April'),
    'south-korea': ('Seoul', 'Korean', 'South Korean Won', '+82', 'March-May and September-November'),
    'sri-lanka': ('Colombo (Sri Jayawardenepura Kotte is the administrative capital)', 'Sinhala and Tamil', 'Sri Lankan Rupee', '+94', 'December-March'),
    'tajikistan': ('Dushanbe', 'Tajik', 'Tajikistani Somoni', '+992', 'May-September'),
    'thailand': ('Bangkok', 'Thai', 'Thai Baht', '+66', 'November-February'),
    'turkey': ('Ankara', 'Turkish', 'Turkish Lira', '+90', 'April-June and September-November'),
    'united-arab-emirates': ('Abu Dhabi', 'Arabic', 'UAE Dirham', '+971', 'November-March'),
    'uzbekistan': ('Tashkent', 'Uzbek', 'Uzbekistani Som', '+998', 'March-May and September-November'),
    'vietnam': ('Hanoi', 'Vietnamese', 'Vietnamese Dong', '+84', 'November-April'),
    'armenia': ('Yerevan', 'Armenian', 'Armenian Dram', '+374', 'May-June and September-October'),
    'azerbaijan': ('Baku', 'Azerbaijani', 'Azerbaijani Manat', '+994', 'April-June and September-October'),
    'cyprus': ('Nicosia', 'Greek and Turkish', 'Euro', '+357', 'April-June and September-October'),
    'georgia': ('Tbilisi', 'Georgian', 'Georgian Lari', '+995', 'May-June and September-October'),
    'iraq': ('Baghdad', 'Arabic and Kurdish', 'Iraqi Dinar', '+964', 'March-May and October-November'),
    'israel': ('Jerusalem', 'Hebrew and Arabic', 'Israeli New Shekel', '+972', 'March-May and September-November'),
    'lebanon': ('Beirut', 'Arabic', 'Lebanese Pound', '+961', 'April-June and September-October'),
    'maldives': ('Malé', 'Dhivehi', 'Maldivian Rufiyaa', '+960', 'November-April'),
    'north-korea': ('Pyongyang', 'Korean', 'North Korean Won', '+850', 'April-June and September-October'),
    'syria': ('Damascus', 'Arabic', 'Syrian Pound', '+963', 'March-May and September-November'),
    'taiwan': ('Taipei', 'Mandarin Chinese', 'New Taiwan Dollar', '+886', 'October-December'),
    'timor-leste': ('Dili', 'Tetum and Portuguese', 'US Dollar', '+670', 'May-November'),
    'turkmenistan': ('Ashgabat', 'Turkmen', 'Turkmenistan Manat', '+993', 'April-June and September-October'),
    'yemen': ('Sana\'a', 'Arabic', 'Yemeni Rial', '+967', 'October-February'),
}

# Descriptions only for the 42 countries NOT already expanded in
# 0012_expand_country_descriptions.py (afghanistan, india, iran, japan,
# pakistan, saudi-arabia, turkey, united-arab-emirates already have real,
# multi-paragraph descriptions).
DESCRIPTIONS = {
    'bahrain': {
        'fa': 'بحرین کشوری جزیره‌ای کوچک در خلیج فارس است که با پلی به عربستان سعودی متصل می‌شود. این کشور که پیش‌تر بر اقتصاد مروارید و سپس نفت متکی بود، امروز به یکی از مراکز مالی و بانکی خاورمیانه تبدیل شده است. منامه، پایتخت بحرین، ترکیبی از برج‌های مدرن و بازارهای سنتی را در کنار هم دارد.\n\nبحرین با تاریخچه‌ای که به تمدن دیلمون باستان بازمی‌گردد، آثار باستانی و قلعه‌های متعددی از جمله قلعه بحرین (ثبت‌شده در یونسکو) دارد و به‌عنوان مقصدی برای گردشگری فرهنگی و تجاری در منطقه شناخته می‌شود.',
        'en': 'Bahrain is a small island nation in the Persian Gulf, connected to Saudi Arabia by a causeway. Once reliant on pearling and later oil, it has become one of the Middle East\'s financial and banking hubs today. Manama, the capital, blends modern towers with traditional souqs.\n\nWith a history tracing back to the ancient Dilmun civilization, Bahrain has numerous archaeological sites and forts, including the UNESCO-listed Bahrain Fort, and is known as a destination for both cultural and business tourism in the region.',
    },
    'bangladesh': {
        'fa': 'بنگلادش کشوری پرجمعیت در دلتای رودخانه‌های گنگ و برهماپوترا در جنوب آسیاست که تقریباً به‌طور کامل توسط هند احاطه شده و در جنوب به خلیج بنگال راه دارد. این کشور یکی از تراکم‌های جمعیتی بالای جهان را دارد و اقتصادش عمدتاً بر صنعت نساجی و پوشاک متکی است.\n\nدهاکا، پایتخت پرجنب‌وجوش این کشور، و سوندربان، بزرگ‌ترین جنگل مانگرو جهان و زیستگاه ببر بنگال، از جاذبه‌های اصلی بنگلادش به‌شمار می‌روند. فرهنگ بنگالی با موسیقی، ادبیات و جشنواره‌های رنگارنگ خود شناخته می‌شود.',
        'en': 'Bangladesh is a densely populated country in the delta of the Ganges and Brahmaputra rivers in South Asia, almost entirely surrounded by India with access to the Bay of Bengal in the south. It has one of the highest population densities in the world, and its economy relies heavily on the textile and garment industry.\n\nDhaka, the country\'s bustling capital, and the Sundarbans, the world\'s largest mangrove forest and home to the Bengal tiger, are among Bangladesh\'s main attractions. Bengali culture is known for its music, literature, and colorful festivals.',
    },
    'bhutan': {
        'fa': 'بوتان کشوری کوچک و کوهستانی در دامنه‌های هیمالیا میان هند و چین است که سیاست منحصربه‌فرد «شادی ناخالص ملی» را به‌جای تولید ناخالص داخلی به‌عنوان معیار توسعه پذیرفته است. این کشور گردشگری را با سیاست «گردشگری کم‌حجم، ارزش بالا» و عوارض روزانه‌ی ورود مدیریت می‌کند.\n\nفرهنگ بودایی بوتان در معابد و صومعه‌های کوهستانی آن مانند صومعه‌ی تاکتسانگ (لانه‌ی ببر) که بر صخره‌ای مرتفع بنا شده، به‌خوبی نمایان است. این کشور با حفظ جنگل‌های وسیع، تعهدی جدی به محیط‌زیست دارد.',
        'en': 'Bhutan is a small, mountainous country in the Himalayas between India and China that has adopted the unique policy of "Gross National Happiness" instead of GDP as its measure of development. It manages tourism through a "high-value, low-volume" policy with a daily entry fee.\n\nBhutan\'s Buddhist culture is vividly present in its mountain temples and monasteries, such as Paro Taktsang (the Tiger\'s Nest), built on a high cliff. The country maintains a serious commitment to the environment through its vast preserved forests.',
    },
    'brunei': {
        'fa': 'برونئی سلطنت‌نشینی کوچک اما ثروتمند در جزیره‌ی بورنئو در جنوب‌شرق آسیاست که اقتصادش تقریباً به‌طور کامل بر ذخایر نفت و گاز طبیعی متکی است. این کشور با سیاست‌های رفاهی گسترده، از جمله آموزش و درمان رایگان، شناخته می‌شود.\n\nمسجد جامع عمر علی سیف‌الدین در بندر سری بگاوان، پایتخت کشور، با گنبد طلاکاری‌شده‌اش نمادی از این کشور است. برونئی همچنین بخش بزرگی از جنگل‌های بارانی بکر بورنئو را در خود حفظ کرده است.',
        'en': 'Brunei is a small but wealthy sultanate on the island of Borneo in Southeast Asia, with an economy almost entirely dependent on oil and natural gas reserves. It is known for extensive welfare policies, including free education and healthcare.\n\nThe Sultan Omar Ali Saifuddien Mosque in Bandar Seri Begawan, the capital, with its gold-leafed dome, is a symbol of the country. Brunei also preserves a large portion of Borneo\'s pristine rainforest.',
    },
    'cambodia': {
        'fa': 'کامبوج کشوری در جنوب‌شرق آسیاست که میراث امپراتوری باستانی خمر را در خود حفظ کرده؛ معبد آنکوروات، بزرگ‌ترین بنای مذهبی جهان، نمادی از این تمدن باستانی و مقصدی محبوب برای گردشگران جهانی است. رودخانه‌ی مکونگ و دریاچه‌ی تونله‌ساپ نقش مهمی در جغرافیا و اقتصاد این کشور دارند.\n\nپس از دوره‌ای دشوار در تاریخ معاصر، کامبوج امروز در حال بازسازی اقتصادی است و گردشگری، نساجی و کشاورزی از ارکان اصلی اقتصاد آن به‌شمار می‌روند. پنوم‌پن، پایتخت کشور، ترکیبی از معماری استعماری فرانسوی و معابد بودایی سنتی را در خود جای داده است.',
        'en': 'Cambodia is a Southeast Asian country that preserves the legacy of the ancient Khmer Empire; Angkor Wat, the largest religious monument in the world, is a symbol of this ancient civilization and a popular destination for global tourists. The Mekong River and Tonlé Sap Lake play an important role in the country\'s geography and economy.\n\nAfter a difficult period in its recent history, Cambodia is today rebuilding economically, with tourism, textiles, and agriculture as key pillars of its economy. Phnom Penh, the capital, combines French colonial architecture with traditional Buddhist temples.',
    },
    'china': {
        'fa': 'چین پرجمعیت‌ترین کشور جهان و یکی از کهن‌ترین تمدن‌های پیوسته‌ی بشری است که در شرق آسیا قرار دارد و با ۱۴ کشور هم‌مرز است — بیشتر از هر کشور دیگر جهان. دیوار بزرگ چین، شهر ممنوعه در پکن، و ارتش تراکوتا از نمادهای شناخته‌شده‌ی تاریخ طولانی این کشورند.\n\nچین امروز دومین اقتصاد بزرگ جهان و قدرتی صنعتی و فناوری پیشرو است. شهرهایی چون پکن (پایتخت)، شانگهای، و شیان (زادگاه ارتش تراکوتا)، ترکیبی از تاریخ باستانی و مدرنیته‌ی خیره‌کننده را به نمایش می‌گذارند.',
        'en': 'China is the world\'s most populous country and one of the oldest continuous civilizations, located in East Asia and bordering 14 countries — more than any other country in the world. The Great Wall of China, the Forbidden City in Beijing, and the Terracotta Army are well-known symbols of its long history.\n\nToday, China is the world\'s second-largest economy and a leading industrial and technological power. Cities such as Beijing (the capital), Shanghai, and Xi\'an (birthplace of the Terracotta Army) showcase a striking blend of ancient history and modernity.',
    },
    'indonesia': {
        'fa': 'اندونزی بزرگ‌ترین کشور جزیره‌ای جهان با بیش از ۱۷ هزار جزیره در جنوب‌شرق آسیاست و پرجمعیت‌ترین کشور مسلمان‌نشین جهان به‌شمار می‌رود. این کشور تنوع قومی و زبانی خارق‌العاده‌ای دارد و صدها زبان محلی در آن رایج است.\n\nبالی با معابد هندو و ساحل‌های زیبایش، بوروبودور بزرگ‌ترین معبد بودایی جهان، و جاکارتا پایتخت پرجمعیت این کشور، از مقاصد اصلی گردشگری اندونزی هستند. اقتصاد این کشور بر منابع طبیعی، کشاورزی و صنعت متکی است.',
        'en': 'Indonesia is the world\'s largest archipelago nation, with over 17,000 islands in Southeast Asia, and is the most populous Muslim-majority country in the world. It has extraordinary ethnic and linguistic diversity, with hundreds of local languages spoken.\n\nBali, with its Hindu temples and beautiful beaches, Borobudur, the world\'s largest Buddhist temple, and Jakarta, the country\'s populous capital, are among Indonesia\'s main tourism destinations. Its economy relies on natural resources, agriculture, and industry.',
    },
    'jordan': {
        'fa': 'اردن کشوری در خاورمیانه با تاریخی غنی است که با عربستان سعودی، عراق، سوریه، اسرائیل و فلسطین هم‌مرز است. پترا، شهر باستانی تراشیده‌شده در صخره‌های سرخ‌رنگ توسط تمدن نبطی، یکی از هفت عجایب جهان نو و شناخته‌شده‌ترین جاذبه‌ی این کشور است.\n\nصحرای وادی‌رم با چشم‌اندازهای مریخ‌گونه‌اش، و دریای مرده، پایین‌ترین نقطه‌ی خشکی روی کره‌ی زمین، از دیگر جاذبه‌های طبیعی اردن‌اند. امان، پایتخت این کشور، ترکیبی از آثار باستانی رومی و شهر مدرن امروزی را در خود جای داده است.',
        'en': 'Jordan is a Middle Eastern country with a rich history, bordering Saudi Arabia, Iraq, Syria, Israel, and Palestine. Petra, the ancient city carved into red sandstone cliffs by the Nabataean civilization, is one of the New Seven Wonders of the World and the country\'s best-known attraction.\n\nThe Wadi Rum desert with its Mars-like landscapes, and the Dead Sea, the lowest point on Earth\'s land surface, are among Jordan\'s other natural attractions. Amman, the capital, combines ancient Roman ruins with a modern contemporary city.',
    },
    'kazakhstan': {
        'fa': 'قزاقستان بزرگ‌ترین کشور محصور در خشکی جهان است که در آسیای مرکزی قرار دارد و از استپ‌های وسیع تا کوه‌های تیان‌شان تنوع جغرافیایی چشمگیری دارد. این کشور که پیش‌تر بخشی از اتحاد جماهیر شوروی بود، پس از استقلال در سال ۱۹۹۱ به یکی از اقتصادهای مهم منطقه به‌ویژه در صادرات نفت و اورانیوم تبدیل شده است.\n\nآستانه (نور-سلطان سابق) پایتخت مدرن این کشور با معماری آینده‌نگرانه است، در حالی که آلماتی به‌عنوان بزرگ‌ترین شهر و مرکز فرهنگی، دامنه‌ی کوه‌های تیان‌شان را در پس‌زمینه‌ی خود دارد.',
        'en': 'Kazakhstan is the world\'s largest landlocked country, located in Central Asia, with striking geographic diversity from vast steppes to the Tian Shan mountains. Once part of the Soviet Union, it has become one of the region\'s key economies since independence in 1991, particularly through oil and uranium exports.\n\nAstana (formerly Nur-Sultan) is the country\'s modern capital with futuristic architecture, while Almaty, the largest city and cultural center, sits against the backdrop of the Tian Shan mountains.',
    },
    'kuwait': {
        'fa': 'کویت کشوری کوچک در شمال خلیج فارس است که یکی از بزرگ‌ترین ذخایر نفتی جهان را در خود دارد و اقتصادش تقریباً به‌طور کامل بر صادرات نفت متکی است. این کشور با عراق و عربستان سعودی هم‌مرز است.\n\nشهر کویت، پایتخت این کشور، با برج‌های کویت (نمادی معماری از دهه‌ی ۱۹۷۰) و اسکای‌لاین مدرنش شناخته می‌شود. کویت یکی از بالاترین سطوح درآمد سرانه‌ی جهان را دارد و به‌عنوان مرکز مالی منطقه نیز شناخته می‌شود.',
        'en': 'Kuwait is a small country at the head of the Persian Gulf, home to one of the world\'s largest oil reserves, with an economy almost entirely dependent on oil exports. It borders Iraq and Saudi Arabia.\n\nKuwait City, the capital, is known for the Kuwait Towers (an architectural icon from the 1970s) and its modern skyline. Kuwait has one of the highest per-capita incomes in the world and is also known as a regional financial center.',
    },
    'kyrgyzstan': {
        'fa': 'قرقیزستان کشوری کوهستانی در آسیای مرکزی است که بیش از نود درصد مساحتش را کوه‌های تیان‌شان و پامیر-آلای پوشانده‌اند. دریاچه‌ی ایسیک‌کول، دومین دریاچه‌ی آب‌شور بزرگ جهان پس از دریای خزر، از مهم‌ترین جاذبه‌های طبیعی این کشور است.\n\nفرهنگ کوچ‌نشینی و سنت‌های ترکی-مغولی در قرقیزستان هنوز زنده است و مسابقات سنتی سوارکاری مانند «کوک‌بورو» بخشی از هویت فرهنگی این مردم به‌شمار می‌رود. بیشکک، پایتخت این کشور، مرکز سیاسی و اقتصادی آن است.',
        'en': 'Kyrgyzstan is a mountainous country in Central Asia, with the Tian Shan and Pamir-Alay ranges covering over ninety percent of its territory. Lake Issyk-Kul, the second-largest saline lake in the world after the Caspian Sea, is one of the country\'s most important natural attractions.\n\nNomadic culture and Turkic-Mongol traditions remain alive in Kyrgyzstan, and traditional horseback competitions such as "Kok-boru" are part of the people\'s cultural identity. Bishkek, the capital, is the country\'s political and economic center.',
    },
    'laos': {
        'fa': 'لائوس تنها کشور محصور در خشکی جنوب‌شرق آسیاست که با رودخانه‌ی مکونگ در مرکز جغرافیای خود، فرهنگی آرام و بودایی دارد. لوانگ‌پرابانگ، پایتخت باستانی این کشور با معابد طلاکاری‌شده‌اش، در فهرست میراث جهانی یونسکو ثبت شده است.\n\nویانتیان، پایتخت کنونی لائوس، مرکز سیاسی و اقتصادی کشور است. اقتصاد لائوس عمدتاً بر کشاورزی، تولید برق آبی و گردشگری متکی است و این کشور یکی از کم‌جمعیت‌ترین کشورهای منطقه به‌شمار می‌رود.',
        'en': 'Laos is the only landlocked country in Southeast Asia, with the Mekong River at the center of its geography and a calm, Buddhist culture. Luang Prabang, the country\'s ancient capital with its gold-leafed temples, is listed as a UNESCO World Heritage Site.\n\nVientiane, Laos\'s current capital, is the country\'s political and economic center. Laos\'s economy relies mainly on agriculture, hydroelectric power, and tourism, and it is one of the least populous countries in the region.',
    },
    'malaysia': {
        'fa': 'مالزی کشوری در جنوب‌شرق آسیا با جمعیتی متنوع از مالایی‌ها، چینی‌ها و هندی‌هاست که این تنوع در آشپزی، معماری و جشن‌های آن به‌وضوح دیده می‌شود. برج‌های دوقلوی پتروناس در کوالالامپور، پایتخت این کشور، زمانی بلندترین ساختمان‌های جهان بودند و همچنان نماد معماری مدرن آسیا به‌شمار می‌روند.\n\nجزیره‌ی بورنئو (بخش مالزیایی آن، شامل صباح و ساراواک) با جنگل‌های بارانی بکر و تنوع زیستی خیره‌کننده‌اش، از مقاصد اکوتوریسم مهم جهان است. اقتصاد مالزی بر صنعت، تجارت الکترونیک و منابع طبیعی متکی است.',
        'en': 'Malaysia is a Southeast Asian country with a diverse population of Malay, Chinese, and Indian communities, a diversity clearly reflected in its cuisine, architecture, and festivals. The Petronas Twin Towers in Kuala Lumpur, the capital, were once the tallest buildings in the world and remain a symbol of modern Asian architecture.\n\nThe island of Borneo (its Malaysian portion, comprising Sabah and Sarawak), with its pristine rainforests and striking biodiversity, is one of the world\'s important ecotourism destinations. Malaysia\'s economy is built on industry, electronics trade, and natural resources.',
    },
    'mongolia': {
        'fa': 'مغولستان کشوری وسیع و کم‌جمعیت در آسیای مرکزی-شرقی است که میان روسیه و چین محصور شده و بخش بزرگی از خاک آن را استپ‌ها و کویر گبی تشکیل می‌دهند. این کشور زادگاه امپراتوری مغول و چنگیزخان است که در قرن سیزدهم بزرگ‌ترین امپراتوری پیوسته‌ی تاریخ را بنا نهاد.\n\nفرهنگ کوچ‌نشینی، زندگی در چادرهای سنتی «گر» و مسابقات سوارکاری هنوز بخش مهمی از هویت مغولستان امروزی‌اند. اولان‌باتور، پایتخت این کشور، سردترین پایتخت جهان و مرکز اصلی اقتصادی و فرهنگی آن است.',
        'en': 'Mongolia is a vast, sparsely populated country in East-Central Asia, sandwiched between Russia and China, with steppes and the Gobi Desert covering much of its territory. It is the birthplace of the Mongol Empire and Genghis Khan, who built the largest contiguous empire in history in the 13th century.\n\nNomadic culture, life in traditional "ger" tents, and horseback competitions remain an important part of Mongolia\'s identity today. Ulaanbaatar, the capital, is the world\'s coldest capital city and the country\'s main economic and cultural center.',
    },
    'myanmar': {
        'fa': 'میانمار (برمه‌ی سابق) کشوری در جنوب‌شرق آسیاست که با هزاران معبد بودایی خود در شهر باستانی باگان، یکی از خیره‌کننده‌ترین مناظر مذهبی جهان را ارائه می‌دهد. این کشور با هند، بنگلادش، چین، لائوس و تایلند هم‌مرز است.\n\nیانگون، بزرگ‌ترین شهر میانمار، میزبان پاگودای طلایی شوداگون، یکی از مقدس‌ترین اماکن بودایی جهان است. نای‌پی‌داو پایتخت اداری کشور است. اقتصاد میانمار بر کشاورزی، منابع طبیعی و صنایع نساجی متکی است.',
        'en': 'Myanmar (formerly Burma) is a Southeast Asian country whose thousands of Buddhist temples in the ancient city of Bagan present one of the most stunning religious landscapes in the world. It borders India, Bangladesh, China, Laos, and Thailand.\n\nYangon, Myanmar\'s largest city, is home to the golden Shwedagon Pagoda, one of the holiest Buddhist sites in the world. Naypyidaw is the country\'s administrative capital. Myanmar\'s economy relies on agriculture, natural resources, and the textile industry.',
    },
    'nepal': {
        'fa': 'نپال کشوری محصور در خشکی میان هند و چین است که در دامنه‌های هیمالیا قرار گرفته و هشت قله از ده قله‌ی بلند جهان، از جمله اورست، بلندترین قله‌ی زمین، در خاک آن یا مرزهایش واقع شده‌اند. این کشور مقصدی محبوب برای کوه‌نوردان و طبیعت‌گردان سراسر جهان است.\n\nکاتماندو، پایتخت نپال، با معابد هندو و بودایی باستانی‌اش از جمله میدان دربار کاتماندو، ترکیبی از معنویت و تاریخ را به نمایش می‌گذارد. لومبینی، زادگاه بودا، نیز در نپال قرار دارد و مقصدی زیارتی مهم برای بودائیان جهان است.',
        'en': 'Nepal is a landlocked country between India and China, situated in the Himalayas, with eight of the world\'s ten highest peaks — including Everest, the world\'s tallest mountain — located within or along its borders. It is a popular destination for mountaineers and nature travelers from around the world.\n\nKathmandu, Nepal\'s capital, showcases a blend of spirituality and history with its ancient Hindu and Buddhist temples, including Kathmandu Durbar Square. Lumbini, the birthplace of Buddha, is also in Nepal and an important pilgrimage destination for Buddhists worldwide.',
    },
    'oman': {
        'fa': 'عمان کشوری در جنوب‌شرقی شبه‌جزیره‌ی عربستان است که با چشم‌اندازهای طبیعی متنوع از کوه‌های الحجر تا صحرای وسیع و سواحل دریای عرب شناخته می‌شود. این کشور برخلاف بسیاری از همسایگانش، تصویری آرام‌تر و سنتی‌تر از فرهنگ عربی را حفظ کرده است.\n\nمسقط، پایتخت عمان، با مسجد جامع سلطان قابوس و قلعه‌های تاریخی‌اش، ترکیبی از معماری اسلامی سنتی و شهر مدرن را ارائه می‌دهد. اقتصاد عمان بر نفت، گاز طبیعی و در سال‌های اخیر گردشگری متکی است.',
        'en': 'Oman is a country in the southeastern Arabian Peninsula, known for its diverse natural landscapes, from the Al Hajar mountains to vast deserts and the Arabian Sea coastline. Unlike many of its neighbors, it has preserved a calmer, more traditional image of Arab culture.\n\nMuscat, Oman\'s capital, with the Sultan Qaboos Grand Mosque and its historic forts, offers a blend of traditional Islamic architecture and a modern city. Oman\'s economy relies on oil, natural gas, and in recent years, tourism.',
    },
    'palestine': {
        'fa': 'فلسطین سرزمینی در خاورمیانه با تاریخی کهن و اهمیت مذهبی ویژه برای سه دین ابراهیمی است. بیت‌لحم، زادگاه عیسی مسیح، و شهر اورشلیم (بیت‌المقدس) با اماکن مقدس متعدد، از مهم‌ترین نقاط این سرزمین به‌شمار می‌روند.\n\nفرهنگ فلسطینی با صنایع‌دستی، آشپزی سنتی و میراث ادبی غنی خود شناخته می‌شود. رام‌الله به‌عنوان مرکز اداری تشکیلات خودگردان فلسطینی عمل می‌کند.',
        'en': 'Palestine is a land in the Middle East with an ancient history and special religious significance for the three Abrahamic faiths. Bethlehem, the birthplace of Jesus Christ, and the city of Jerusalem, with its many holy sites, are among the most important places in this land.\n\nPalestinian culture is known for its handicrafts, traditional cuisine, and rich literary heritage. Ramallah serves as the administrative center of the Palestinian Authority.',
    },
    'philippines': {
        'fa': 'فیلیپین کشوری جزیره‌ای در جنوب‌شرق آسیا با بیش از ۷۰۰۰ جزیره است که تنوع فرهنگی آن ترکیبی از میراث مالایی، اسپانیایی و آمریکایی را نشان می‌دهد. این کشور تنها کشور آسیایی با اکثریت مسیحی است.\n\nمانیل، پایتخت پرجمعیت این کشور، و جزایر گردشگری مانند بوراکای و پالاوان با سواحل و آب‌های فیروزه‌ای‌شان، از مقاصد اصلی گردشگری فیلیپین‌اند. اقتصاد این کشور بر خدمات، صنعت و کشاورزی متکی است.',
        'en': 'The Philippines is an island nation in Southeast Asia with over 7,000 islands, whose cultural diversity reflects a blend of Malay, Spanish, and American heritage. It is the only Asian country with a Christian majority.\n\nManila, the country\'s populous capital, and tourist islands such as Boracay and Palawan with their turquoise waters and beaches, are among the Philippines\' main tourism destinations. The country\'s economy relies on services, industry, and agriculture.',
    },
    'qatar': {
        'fa': 'قطر شبه‌جزیره‌ای کوچک در خلیج فارس است که با ذخایر عظیم گاز طبیعی، یکی از بالاترین سرانه‌های درآمد جهان را دارد. این کشور با میزبانی جام جهانی فوتبال ۲۰۲۲، توجه جهانی گسترده‌ای را به خود جلب کرد.\n\nدوحه، پایتخت قطر، با اسکای‌لاین مدرن، موزه‌های هنری معتبر مانند موزه‌ی هنر اسلامی، و بازار سنتی سوق واقف، ترکیبی از سنت و مدرنیته را ارائه می‌دهد.',
        'en': 'Qatar is a small peninsula in the Persian Gulf that, with its massive natural gas reserves, has one of the highest per-capita incomes in the world. The country drew widespread global attention by hosting the 2022 FIFA World Cup.\n\nDoha, Qatar\'s capital, with its modern skyline, prestigious art museums such as the Museum of Islamic Art, and the traditional Souq Waqif, offers a blend of tradition and modernity.',
    },
    'russia': {
        'fa': 'روسیه بزرگ‌ترین کشور جهان از نظر مساحت است که در دو قاره‌ی اروپا و آسیا گسترده شده و با ۱۴ کشور هم‌مرز است. این کشور با تاریخی غنی از دوران امپراتوری تزاری تا اتحاد جماهیر شوروی، میراث فرهنگی و هنری عظیمی از جمله ادبیات، باله و موسیقی کلاسیک بر جای گذاشته است.\n\nمسکو، پایتخت روسیه، با کرملین و میدان سرخ، و سن‌پترزبورگ با کاخ‌های تزاری و موزه‌ی ارمیتاژ، از مهم‌ترین مقاصد گردشگری این کشورند. سیبری با وسعت بی‌کران و دریاچه‌ی بایکال، عمیق‌ترین دریاچه‌ی جهان، از شگفتی‌های طبیعی روسیه به‌شمار می‌روند.',
        'en': 'Russia is the largest country in the world by area, spanning two continents — Europe and Asia — and bordering 14 countries. With a rich history from the Tsarist Empire to the Soviet Union, it has left behind an immense cultural and artistic legacy, including literature, ballet, and classical music.\n\nMoscow, the capital, with the Kremlin and Red Square, and Saint Petersburg with its Tsarist palaces and the Hermitage Museum, are among the country\'s most important tourist destinations. Siberia, with its immense expanse, and Lake Baikal, the world\'s deepest lake, are among Russia\'s natural wonders.',
    },
    'singapore': {
        'fa': 'سنگاپور شهر-کشوری کوچک اما بسیار پیشرفته در جنوب‌شرق آسیاست که از یک بندر تجاری کوچک به یکی از مراکز مالی و تجاری بزرگ جهان تبدیل شده است. این کشور با نظافت شهری، امنیت بالا و برنامه‌ریزی شهری پیشرفته‌اش شناخته می‌شود.\n\nباغ‌های خلیج (گاردنز بای‌د بی) با درختان مصنوعی غول‌پیکرش، مارینا بی‌سندز با استخر بی‌کران روی پشت‌بام، و محله‌های چندفرهنگی مانند چاینا‌تاون و لیتل ایندیا، تصویری از تنوع و نوآوری سنگاپور ارائه می‌دهند.',
        'en': 'Singapore is a small but highly developed city-state in Southeast Asia that has grown from a small trading port into one of the world\'s major financial and commercial hubs. It is known for its urban cleanliness, high safety standards, and advanced city planning.\n\nGardens by the Bay with its giant Supertrees, Marina Bay Sands with its rooftop infinity pool, and multicultural neighborhoods such as Chinatown and Little India, showcase Singapore\'s diversity and innovation.',
    },
    'south-korea': {
        'fa': 'کره جنوبی کشوری در شرق آسیاست که در دهه‌های اخیر از اقتصادی کشاورزی به یکی از قدرت‌های صنعتی و فناوری برتر جهان تبدیل شده — پدیده‌ای که به «معجزه‌ی رودخانه‌ی هان» معروف است. این کشور زادگاه شرکت‌های بزرگی چون سامسونگ و هیوندای است.\n\nسئول، پایتخت پویای این کشور، ترکیبی از کاخ‌های سلسله‌ی جوسان مانند کاخ گیونگ‌بوک‌گونگ و محله‌های فناوری‌محور مدرن را ارائه می‌دهد. فرهنگ پاپ کره‌ای (K-pop) و سینمای کره‌ای در سال‌های اخیر شهرت جهانی یافته‌اند.',
        'en': 'South Korea is an East Asian country that transformed in recent decades from an agricultural economy into one of the world\'s leading industrial and technological powers — a phenomenon known as the "Miracle on the Han River." It is home to major companies such as Samsung and Hyundai.\n\nSeoul, the country\'s dynamic capital, offers a blend of Joseon Dynasty palaces such as Gyeongbokgung and modern tech-driven districts. Korean pop culture (K-pop) and Korean cinema have gained worldwide fame in recent years.',
    },
    'sri-lanka': {
        'fa': 'سری‌لانکا کشوری جزیره‌ای در اقیانوس هند، در نزدیکی جنوب هند است که به‌خاطر چای، ادویه‌جات و سواحل زیبایش شهرت دارد. این کشور با تاریخی طولانی از پادشاهی‌های سینهالی، میراث بودایی غنی از جمله معبد دندان مقدس در کندی را در خود حفظ کرده است.\n\nمزارع چای در فلات‌های مرتفع، فیل‌های وحشی در پارک‌های ملی، و سواحل جنوبی این جزیره، سری‌لانکا را به مقصدی محبوب برای طبیعت‌گردی و آرامش تبدیل کرده‌اند.',
        'en': 'Sri Lanka is an island nation in the Indian Ocean, near the southern tip of India, renowned for its tea, spices, and beautiful beaches. With a long history of Sinhalese kingdoms, it preserves a rich Buddhist heritage, including the Temple of the Sacred Tooth Relic in Kandy.\n\nTea plantations on its highland plateaus, wild elephants in national parks, and the island\'s southern beaches have made Sri Lanka a popular destination for nature tourism and relaxation.',
    },
    'tajikistan': {
        'fa': 'تاجیکستان کشوری کوهستانی و محصور در خشکی در آسیای مرکزی است که بیش از نود درصد مساحتش را کوه‌های پامیر و تیان‌شان پوشانده‌اند و آن را به یکی از کوهستانی‌ترین کشورهای جهان تبدیل کرده‌اند. زبان تاجیکی، گویشی از فارسی است که پیوند فرهنگی عمیقی با ایران و افغانستان دارد.\n\nمنطقه‌ی پامیر با «بام جهان» ملقب شده و مقصدی برای کوه‌نوردان و طبیعت‌گردان است. دوشنبه، پایتخت این کشور، مرکز سیاسی و فرهنگی تاجیکستان به‌شمار می‌رود.',
        'en': 'Tajikistan is a mountainous, landlocked country in Central Asia, with the Pamir and Tian Shan ranges covering over ninety percent of its territory, making it one of the most mountainous countries in the world. The Tajik language is a dialect of Persian, reflecting deep cultural ties with Iran and Afghanistan.\n\nThe Pamir region, nicknamed the "Roof of the World," is a destination for mountaineers and nature travelers. Dushanbe, the capital, is the country\'s political and cultural center.',
    },
    'thailand': {
        'fa': 'تایلند کشوری در جنوب‌شرق آسیاست که تنها کشور منطقه است که هرگز مستعمره‌ی قدرت‌های اروپایی نشده. این کشور با معابد بودایی طلاکاری‌شده، کاخ‌های سلطنتی و سواحل استوایی‌اش، یکی از پربازدیدترین مقاصد گردشگری جهان به‌شمار می‌رود.\n\nبانکوک، پایتخت پرجنب‌وجوش این کشور، با کاخ بزرگ و معبد بودای زمردین، و جزایر جنوبی مانند پوکت و کوساموئی، تصویری از تنوع فرهنگی و طبیعی تایلند ارائه می‌دهند. اقتصاد این کشور بر گردشگری، صنعت و کشاورزی متکی است.',
        'en': 'Thailand is a Southeast Asian country and the only one in the region never colonized by a European power. With its gold-leafed Buddhist temples, royal palaces, and tropical beaches, it is one of the world\'s most visited tourist destinations.\n\nBangkok, the country\'s bustling capital, with the Grand Palace and the Emerald Buddha Temple, and southern islands such as Phuket and Koh Samui, showcase Thailand\'s cultural and natural diversity. Its economy relies on tourism, industry, and agriculture.',
    },
    'uzbekistan': {
        'fa': 'ازبکستان کشوری در آسیای مرکزی است که در طول تاریخ در مسیر اصلی جاده ابریشم قرار داشته و شهرهایی چون سمرقند، بخارا و خیوه از آن دوران، میراث معماری اسلامی خیره‌کننده‌ای برای امروز به‌جا گذاشته‌اند. مسجدها و مدرسه‌های کاشی‌کاری‌شده‌ی این شهرها از شاهکارهای معماری تیموری‌اند.\n\nتاشکند، پایتخت مدرن این کشور، مرکز سیاسی و اقتصادی ازبکستان است. این کشور در سال‌های اخیر تلاش کرده با اصلاحات اقتصادی و گشایش گردشگری، میراث تاریخی خود را به دنیا معرفی کند.',
        'en': 'Uzbekistan is a Central Asian country that historically sat on the main route of the Silk Road, and cities such as Samarkand, Bukhara, and Khiva from that era have left behind a stunning Islamic architectural legacy for today. The tiled mosques and madrasas of these cities are masterpieces of Timurid architecture.\n\nTashkent, the country\'s modern capital, is Uzbekistan\'s political and economic center. In recent years, the country has pursued economic reforms and tourism openness to introduce its historical heritage to the world.',
    },
    'vietnam': {
        'fa': 'ویتنام کشوری کشیده در جنوب‌شرق آسیاست که از دلتای رودخانه‌ی مکونگ در جنوب تا کوهستان‌های شمالی امتداد دارد. این کشور با تاریخی پرفراز و نشیب از جمله دوران استعمار فرانسه و جنگ ویتنام، امروز یکی از اقتصادهای به‌سرعت در حال رشد آسیاست.\n\nخلیج‌ هالونگ با هزاران صخره‌ی آهکی برخاسته از دریا، هانوی پایتخت با معماری استعماری فرانسوی، و هوشی‌مین‌سیتی (سایگون سابق) به‌عنوان مرکز اقتصادی کشور، از جاذبه‌های اصلی ویتنام‌اند.',
        'en': 'Vietnam is an elongated Southeast Asian country stretching from the Mekong Delta in the south to the mountains of the north. With a turbulent history including French colonization and the Vietnam War, it is today one of Asia\'s fastest-growing economies.\n\nHa Long Bay with its thousands of limestone karsts rising from the sea, Hanoi, the capital, with its French colonial architecture, and Ho Chi Minh City (formerly Saigon) as the country\'s economic center, are among Vietnam\'s main attractions.',
    },
    'armenia': {
        'fa': 'ارمنستان کشوری محصور در خشکی در قفقاز جنوبی است و نخستین کشوری در جهان به‌شمار می‌رود که مسیحیت را به‌عنوان دین رسمی خود پذیرفت (سال ۳۰۱ میلادی). این میراث مسیحی در صومعه‌ها و کلیساهای باستانی سراسر این کشور، از جمله صومعه‌ی گقارد، به‌وضوح دیده می‌شود.\n\nکوه آرارات، هرچند امروز در خاک ترکیه قرار دارد، همچنان نماد ملی و فرهنگی ارمنی‌ها به‌شمار می‌رود و از دوردست در افق ایروان، پایتخت این کشور، دیده می‌شود.',
        'en': 'Armenia is a landlocked country in the South Caucasus and is considered the first country in the world to adopt Christianity as its official religion (in 301 AD). This Christian heritage is clearly visible in the ancient monasteries and churches across the country, including Geghard Monastery.\n\nMount Ararat, although today located within Turkey\'s borders, remains a national and cultural symbol for Armenians and can be seen from afar on the horizon of Yerevan, the country\'s capital.',
    },
    'azerbaijan': {
        'fa': 'آذربایجان کشوری در قفقاز جنوبی و کناره‌ی دریای خزر است که به‌خاطر ذخایر نفتی‌اش از قرن نوزدهم به یکی از مراکز مهم صنعت نفت جهان تبدیل شد. باکو، پایتخت این کشور، ترکیبی خیره‌کننده از برج‌های شعله (فلیم تاورز) مدرن و شهر باستانی باروداری (ایچری‌شهر) را ارائه می‌دهد.\n\nاین کشور با فرهنگی ترکی-قفقازی، موسیقی مقام سنتی و صنایع‌دستی فرش، میراث غنی خود را حفظ کرده و در سال‌های اخیر با رویدادهایی چون مسابقات فرمول یک و اروویژن، توجه جهانی را جلب کرده است.',
        'en': 'Azerbaijan is a South Caucasus country on the shores of the Caspian Sea that, due to its oil reserves, became one of the world\'s important oil industry centers from the 19th century onward. Baku, the capital, offers a striking blend of modern Flame Towers and the ancient walled Old City (Icherisheher).\n\nWith a Turkic-Caucasian culture, traditional mugham music, and carpet handicrafts, the country preserves its rich heritage and has drawn global attention in recent years through events such as Formula 1 races and Eurovision.',
    },
    'cyprus': {
        'fa': 'قبرس جزیره‌ای در شرق دریای مدیترانه است که از نظر سیاسی میان بخش یونانی‌نشین در جنوب و بخش ترک‌نشین در شمال تقسیم شده است. این جزیره با تاریخی که به دوران باستان یونان و روم بازمی‌گردد، آثار باستانی متعددی از جمله مکان‌های ثبت‌شده در یونسکو دارد.\n\nنیکوزیا، پایتخت تقسیم‌شده‌ی این جزیره، تنها پایتخت دوبخشی جهان است. قبرس با سواحل آفتابی مدیترانه‌ای‌اش، مقصدی محبوب برای گردشگری تابستانی اروپاست.',
        'en': 'Cyprus is an island in the eastern Mediterranean, politically divided between the Greek-Cypriot south and the Turkish-Cypriot north. With a history dating back to ancient Greece and Rome, the island has numerous archaeological sites, including several UNESCO-listed locations.\n\nNicosia, the island\'s divided capital, is the world\'s only capital city split in two. With its sunny Mediterranean beaches, Cyprus is a popular destination for European summer tourism.',
    },
    'georgia': {
        'fa': 'گرجستان کشوری در قفقاز جنوبی میان دریای سیاه و کوه‌های قفقاز است که به‌خاطر طبیعت کوهستانی، شراب‌سازی باستانی (که قدمتش به هشت هزار سال می‌رسد) و مهمان‌نوازی معروف است. این کشور یکی از نخستین کشورهای مسیحی جهان به‌شمار می‌رود.\n\nتفلیس، پایتخت این کشور، با معماری قدیمی و چشمه‌های آب‌گرم گوگردی‌اش، و منطقه‌ی کوهستانی سوانتی با برج‌های سنگی قرون‌وسطایی‌اش، از جاذبه‌های اصلی گرجستان‌اند.',
        'en': 'Georgia is a South Caucasus country between the Black Sea and the Caucasus Mountains, known for its mountainous nature, ancient winemaking tradition (dating back eight thousand years), and famed hospitality. It is one of the world\'s earliest Christian nations.\n\nTbilisi, the capital, with its old architecture and sulfur hot springs, and the mountainous Svaneti region with its medieval stone towers, are among Georgia\'s main attractions.',
    },
    'iraq': {
        'fa': 'عراق کشوری در خاورمیانه و زادگاه تمدن بین‌النهرین است — سرزمینی که خط، قانون‌نویسی و شهرنشینی نخستین‌بار در آن شکل گرفت. بابل باستانی، اور و نینوا از شهرهای تاریخی این سرزمین‌اند که میراث سومری، بابلی و آشوری را در خود دارند.\n\nبغداد، پایتخت این کشور، در دوران عباسیان مرکز علم و فرهنگ جهان اسلام بود. عراق پس از دهه‌ها جنگ و بی‌ثباتی، امروز در مسیر بازسازی است و کربلا و نجف از مقاصد مهم زیارتی شیعیان جهان به‌شمار می‌روند.',
        'en': 'Iraq is a Middle Eastern country and the birthplace of Mesopotamian civilization — the land where writing, law codes, and urban life first emerged. Ancient Babylon, Ur, and Nineveh are historic cities here, carrying Sumerian, Babylonian, and Assyrian heritage.\n\nBaghdad, the capital, was the center of science and culture in the Islamic world during the Abbasid era. After decades of war and instability, Iraq is today on a path of reconstruction, and Karbala and Najaf are important pilgrimage destinations for Shia Muslims worldwide.',
    },
    'israel': {
        'fa': 'اسرائیل کشوری در خاورمیانه با اهمیت مذهبی بی‌نظیر برای یهودیت، مسیحیت و اسلام است. اورشلیم (بیت‌المقدس) با دیوار غربی، کلیسای قیامت و مسجد الاقصی، یکی از مقدس‌ترین نقاط جهان برای هر سه دین ابراهیمی به‌شمار می‌رود.\n\nتل‌آویو به‌عنوان مرکز اقتصادی و فناوری این کشور، و دریای مرده که پایین‌ترین نقطه‌ی خشکی زمین است، از دیگر نقاط شاخص اسرائیل‌اند. اقتصاد این کشور بر فناوری پیشرفته، گردشگری مذهبی و کشاورزی متکی است.',
        'en': 'Israel is a Middle Eastern country of unique religious significance for Judaism, Christianity, and Islam. Jerusalem, with the Western Wall, the Church of the Holy Sepulchre, and the Al-Aqsa Mosque, is one of the holiest places in the world for all three Abrahamic faiths.\n\nTel Aviv, as the country\'s economic and technology hub, and the Dead Sea, the lowest point on Earth\'s land surface, are among Israel\'s other notable sites. The country\'s economy relies on advanced technology, religious tourism, and agriculture.',
    },
    'lebanon': {
        'fa': 'لبنان کشوری کوچک در ساحل شرقی دریای مدیترانه است که تاریخی غنی از تمدن فنیقی باستان تا امروز دارد. این کشور با تنوع مذهبی و فرقه‌ای خود، و همچنین با آشپزی مشهور جهانی‌اش، شناخته می‌شود.\n\nبیروت، پایتخت این کشور که زمانی «پاریس خاورمیانه» لقب گرفته بود، و معابد باستانی بعلبک از دوران روم، از جاذبه‌های اصلی لبنان‌اند. این کشور علی‌رغم چالش‌های اقتصادی و سیاسی، همچنان میراث فرهنگی غنی خود را حفظ کرده است.',
        'en': 'Lebanon is a small country on the eastern Mediterranean coast with a rich history from ancient Phoenician civilization to today. It is known for its religious and sectarian diversity, as well as its world-famous cuisine.\n\nBeirut, the capital, once nicknamed the "Paris of the Middle East," and the ancient Roman-era temples of Baalbek, are among Lebanon\'s main attractions. Despite economic and political challenges, the country continues to preserve its rich cultural heritage.',
    },
    'maldives': {
        'fa': 'مالدیو مجموعه‌ای از حدود ۱۲۰۰ جزیره‌ی مرجانی در اقیانوس هند است که به‌خاطر آب‌های فیروزه‌ای، ویلاهای روی آب و صخره‌های مرجانی‌اش، یکی از مشهورترین مقاصد گردشگری لوکس و ماه‌عسل جهان به‌شمار می‌رود. این کشور کوتاه‌ترین ارتفاع متوسط از سطح دریا را در میان کشورهای جهان دارد.\n\nماله، پایتخت کوچک و پرتراکم این کشور، مرکز اداری و اقتصادی مالدیو است. اقتصاد این کشور تقریباً به‌طور کامل بر گردشگری و صید ماهی متکی است.',
        'en': 'The Maldives is an archipelago of about 1,200 coral islands in the Indian Ocean, renowned for its turquoise waters, overwater villas, and coral reefs, making it one of the world\'s most famous luxury and honeymoon destinations. It has the lowest average elevation above sea level of any country in the world.\n\nMalé, the country\'s small, densely populated capital, is the Maldives\' administrative and economic center. The country\'s economy relies almost entirely on tourism and fishing.',
    },
    'north-korea': {
        'fa': 'کره شمالی کشوری در شرق آسیاست که از سال ۱۹۴۸ تحت حکومتی متمرکز و منزوی از جامعه‌ی جهانی اداره می‌شود. این کشور با کره جنوبی، چین و روسیه هم‌مرز است و دسترسی گردشگران خارجی به آن به‌شدت محدود و کنترل‌شده است.\n\nپیونگ‌یانگ، پایتخت این کشور، با میدان‌ها و بناهای یادبود عظیم دولتی‌اش شناخته می‌شود. اقتصاد کره شمالی عمدتاً دولتی و متمرکز است.',
        'en': 'North Korea is an East Asian country that has been governed under a centralized system, isolated from the international community, since 1948. It borders South Korea, China, and Russia, and foreign tourist access is heavily restricted and controlled.\n\nPyongyang, the capital, is known for its vast state monuments and public squares. North Korea\'s economy is largely state-run and centrally planned.',
    },
    'syria': {
        'fa': 'سوریه کشوری در خاورمیانه با تاریخی بسیار کهن است؛ دمشق، پایتخت این کشور، یکی از قدیمی‌ترین شهرهای پیوسته مسکونی جهان به‌شمار می‌رود. این سرزمین در طول تاریخ میزبان تمدن‌های آرامی، رومی، بیزانسی و اسلامی بوده است.\n\nپالمیرا، شهر باستانی کاروان‌سالار در دل کویر سوریه، و بازارهای سرپوشیده‌ی تاریخی دمشق و حلب، بخشی از میراث غنی این کشورند که بسیاری از آن‌ها در سال‌های اخیر آسیب دیده‌اند. سوریه امروز در مسیر بازسازی پس از دوران طولانی جنگ است.',
        'en': 'Syria is a Middle Eastern country with an extremely ancient history; Damascus, its capital, is considered one of the oldest continuously inhabited cities in the world. This land has historically hosted Aramaic, Roman, Byzantine, and Islamic civilizations.\n\nPalmyra, the ancient caravan city in the heart of the Syrian desert, and the historic covered markets of Damascus and Aleppo, are part of the country\'s rich heritage, much of which has been damaged in recent years. Syria is today on a path of reconstruction after a long period of war.',
    },
    'taiwan': {
        'fa': 'تایوان جزیره‌ای در شرق آسیا در نزدیکی سواحل چین است که با اقتصادی پیشرفته و صنعت نیمه‌هادی‌های جهانی خود (از جمله بزرگ‌ترین تولیدکننده‌ی تراشه‌ی جهان) شناخته می‌شود. این جزیره کوهستانی با معابد بودایی-تائوئیستی و بازارهای شبانه‌ی پرجنب‌وجوش خود فرهنگی غنی دارد.\n\nتایپه، پایتخت این جزیره، با برج تایپه ۱۰۱ (که زمانی بلندترین ساختمان جهان بود) و موزه‌ی کاخ ملی که یکی از بزرگ‌ترین مجموعه‌های هنر چینی جهان را در خود جای داده، از جاذبه‌های اصلی تایوان است.',
        'en': 'Taiwan is an island in East Asia near the coast of China, known for its advanced economy and its role as a global semiconductor powerhouse (including being home to the world\'s largest chip manufacturer). This mountainous island has a rich culture reflected in its Buddhist-Taoist temples and lively night markets.\n\nTaipei, the island\'s capital, with Taipei 101 (once the world\'s tallest building) and the National Palace Museum, home to one of the world\'s largest collections of Chinese art, is among Taiwan\'s main attractions.',
    },
    'timor-leste': {
        'fa': 'تیمور شرقی کوچک‌ترین کشور آسیای جنوب‌شرقی است که پس از سال‌ها استعمار پرتغال و سپس اشغال، در سال ۲۰۰۲ به استقلال کامل رسید — این کشور یکی از جوان‌ترین ملت‌های جهان به‌شمار می‌رود. زبان‌های رسمی آن، تتوم و پرتغالی، میراث استعماری این سرزمین را نشان می‌دهند.\n\nدیلی، پایتخت این کشور، مرکز کوچک اما رو‌به‌رشد سیاسی و اقتصادی تیمور شرقی است. طبیعت بکر این کشور، از جمله آب‌های مناسب غواصی، پتانسیل گردشگری در حال توسعه‌ای را برای آن رقم زده است.',
        'en': 'Timor-Leste is the smallest country in Southeast Asia, which, after years of Portuguese colonization and subsequent occupation, achieved full independence in 2002 — making it one of the world\'s youngest nations. Its official languages, Tetum and Portuguese, reflect the land\'s colonial heritage.\n\nDili, the capital, is a small but growing political and economic center for Timor-Leste. The country\'s pristine nature, including waters well suited for diving, has given it a developing tourism potential.',
    },
    'turkmenistan': {
        'fa': 'ترکمنستان کشوری در آسیای مرکزی است که بیشتر مساحتش را کویر قره‌قوم پوشانده و به‌خاطر ذخایر گاز طبیعی عظیم خود شناخته می‌شود. عشق‌آباد، پایتخت این کشور، با ساختمان‌های مرمرین سفید و معماری یکدست باشکوهش، رکورد جهانی بیشترین تراکم ساختمان‌های پوشیده از مرمر سفید را در اختیار دارد.\n\nدروازه‌ی جهنم در نزدیکی درواز، حفره‌ای گازی که دهه‌هاست در حال سوختن است، از عجیب‌ترین جاذبه‌های گردشگری این کشور به‌شمار می‌رود.',
        'en': 'Turkmenistan is a Central Asian country whose territory is mostly covered by the Karakum Desert, known for its vast natural gas reserves. Ashgabat, the capital, with its white marble buildings and uniformly grand architecture, holds a world record for the highest concentration of white marble-clad buildings.\n\nThe "Door to Hell" near Darvaza, a gas crater that has been burning for decades, is one of the country\'s most unusual tourist attractions.',
    },
    'yemen': {
        'fa': 'یمن کشوری در جنوب شبه‌جزیره‌ی عربستان است که تاریخی کهن به‌عنوان «عربستان خوشبخت» در دوران باستان دارد. صنعا، پایتخت این کشور با خانه‌های برجی خشتی چندطبقه‌اش در بافت قدیمی شهر، یکی از منحصربه‌فردترین مناظر معماری جهان اسلام است.\n\nجزیره‌ی سقطری، با گیاهان و جانوران بومی منحصربه‌فردش از جمله درخت خون‌اژدها، یکی از شگفت‌انگیزترین اکوسیستم‌های جدا‌افتاده‌ی جهان به‌شمار می‌رود. یمن سال‌هاست درگیر بحران انسانی و ناآرامی است.',
        'en': 'Yemen is a country at the southern tip of the Arabian Peninsula with an ancient history as "Arabia Felix" in antiquity. Sana\'a, the capital, with its multi-story mudbrick tower houses in the old city, presents one of the most distinctive architectural landscapes in the Islamic world.\n\nSocotra Island, with its unique endemic flora and fauna, including the dragon\'s blood tree, is one of the world\'s most remarkable isolated ecosystems. Yemen has faced years of humanitarian crisis and unrest.',
    },
}


def apply_facts_and_descriptions(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    for slug, (capital, lang, currency, code, best_time) in FACTS.items():
        capital_en, lang_en, currency_en, code_en, best_time_en = FACTS_EN[slug]
        update_kwargs = dict(
            capital=capital, capital_fa=capital, capital_en=capital_en,
            official_language=lang, official_language_fa=lang, official_language_en=lang_en,
            currency=currency, currency_fa=currency, currency_en=currency_en,
            calling_code=code,
            best_time_to_visit=best_time, best_time_to_visit_fa=best_time, best_time_to_visit_en=best_time_en,
        )
        if slug in DESCRIPTIONS:
            update_kwargs.update(
                description=DESCRIPTIONS[slug]['fa'],
                description_fa=DESCRIPTIONS[slug]['fa'],
                description_en=DESCRIPTIONS[slug]['en'],
            )
        Country.objects.filter(slug=slug).update(**update_kwargs)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_country_quickfacts'),
    ]

    operations = [
        migrations.RunPython(apply_facts_and_descriptions, noop),
    ]
