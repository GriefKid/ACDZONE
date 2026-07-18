# Seeds the four season weather blurbs (fa + en) added in
# 0023_country_weather_fields for every country already in the table.
# General, traveler-oriented climate descriptions — not live weather data
# (see Country.weather_* help/model comment) — an admin can always
# override any of these later from /admin/.
from django.db import migrations

# slug -> {season: (fa_text, en_text)}
WEATHER = {
    'afghanistan': {
        'spring': ('بهاری معتدل و سرسبز با گل‌های وحشی در دره‌ها؛ بهترین فصل برای گردش.', 'Mild, green spring with wildflowers in the valleys — the best season to visit.'),
        'summer': ('تابستان گرم و خشک در دشت‌ها، اما کوهستان‌های مرکزی خنک‌تر و دلپذیرند.', 'Hot, dry summer on the plains, while the central highlands stay cooler.'),
        'autumn': ('پاییز خشک و آفتابی با هوای رو به سردی، مناسب سفرهای کوهستانی.', 'Dry, sunny autumn turning cool — good for mountain travel.'),
        'winter': ('زمستان سرد و برفی به‌ویژه در ارتفاعات؛ برخی جاده‌های کوهستانی بسته می‌شوند.', 'Cold, snowy winter, especially in the highlands; some mountain roads close.'),
    },
    'armenia': {
        'spring': ('بهار خنک و بارانی با طبیعتی سرسبز در دامنه‌های آرارات.', 'Cool, rainy spring with lush greenery around Mount Ararat.'),
        'summer': ('تابستان گرم و خشک در ایروان، اما مناطق کوهستانی خنک باقی می‌مانند.', 'Hot, dry summer in Yerevan, while mountain areas stay cool.'),
        'autumn': ('پاییز طلایی و ملایم، فصل برداشت انگور و بهترین زمان بازدید.', 'Golden, mild autumn — grape-harvest season and the best time to visit.'),
        'winter': ('زمستان سرد با برف فراوان در ارتفاعات، مناسب اسکی.', 'Cold winter with heavy snow in the highlands, good for skiing.'),
    },
    'azerbaijan': {
        'spring': ('بهاری معتدل و پرگل، هوای دلپذیر در باکو و اطراف.', 'Mild, flowery spring with pleasant weather around Baku.'),
        'summer': ('تابستان گرم و شرجی در سواحل خزر، خنک‌تر در کوهستان قفقاز.', 'Hot, humid summer on the Caspian coast, cooler in the Caucasus mountains.'),
        'autumn': ('پاییز ملایم و آفتابی، یکی از بهترین فصل‌های سفر.', 'Mild, sunny autumn — one of the best seasons to travel.'),
        'winter': ('زمستان خنک و مرطوب در باکو، سرد و برفی در کوهستان‌ها.', 'Cool, damp winter in Baku; cold and snowy in the mountains.'),
    },
    'bahrain': {
        'spring': ('بهار گرم و مطبوع، مناسب‌ترین فصل برای گردش در فضای باز.', 'Warm, pleasant spring — the best season for outdoor sightseeing.'),
        'summer': ('تابستان بسیار گرم و مرطوب با دمای بالای ۴۰ درجه.', 'Very hot, humid summer with temperatures above 40°C.'),
        'autumn': ('پاییز به‌تدریج خنک‌تر می‌شود اما همچنان گرم و شرجی است.', 'Autumn gradually cools but remains warm and humid.'),
        'winter': ('زمستان معتدل و خوشایند، بهترین زمان سفر به بحرین.', 'Mild, pleasant winter — the best time to visit Bahrain.'),
    },
    'bangladesh': {
        'spring': ('بهار گرم پیش از فصل باران، هوایی خشک‌تر نسبت به تابستان.', 'Warm pre-monsoon spring, drier than summer.'),
        'summer': ('تابستان گرم و پرباران با موسمی‌های سیل‌آسا.', 'Hot summer with heavy monsoon rains.'),
        'autumn': ('پاییز مرطوب با بارش‌های پراکنده در ابتدای فصل.', 'Humid autumn with scattered rain early in the season.'),
        'winter': ('زمستان خنک و خشک، مطبوع‌ترین فصل برای سفر.', 'Cool, dry winter — the most pleasant travel season.'),
    },
    'bhutan': {
        'spring': ('بهار با رودودندرون‌های شکوفا، هوای خنک کوهستانی و آسمان صاف.', 'Spring with blooming rhododendrons, cool mountain air and clear skies.'),
        'summer': ('تابستان بارانی موسمی، دره‌ها سرسبز اما مسیرهای کوهستانی گاه گلی‌اند.', 'Rainy monsoon summer — valleys are lush but trails can be muddy.'),
        'autumn': ('پاییز صاف و خنک با بهترین دید به قله‌های هیمالیا؛ فصل طلایی گردشگری.', 'Clear, crisp autumn with the best Himalayan views — peak tourist season.'),
        'winter': ('زمستان سرد و آفتابی در دره‌ها، برف سنگین در ارتفاعات بالا.', 'Cold, sunny winter in the valleys, heavy snow at high altitude.'),
    },
    'brunei': {
        'spring': ('آب‌وهوای استوایی گرم و مرطوب تقریباً یکسان در تمام سال، با احتمال باران در هر زمان.', 'Warm, humid equatorial climate is almost the same year-round, with rain possible any time.'),
        'summer': ('گرم و مرطوب با رطوبت بالا، بارش‌های ناگهانی بعدازظهر رایج است.', 'Hot and humid with sudden afternoon downpours common.'),
        'autumn': ('همچنان گرم و مرطوب؛ اواخر سال معمولاً پربارش‌تر است.', 'Still hot and humid; later months tend to be wetter.'),
        'winter': ('فصل بارانی‌تر سال (نوامبر تا ژانویه) اما دما همچنان بالا می‌ماند.', 'The wetter part of the year (Nov–Jan), though temperatures stay high.'),
    },
    'cambodia': {
        'spring': ('بهار بسیار گرم و خشک، اوج گرما پیش از شروع باران‌ها.', 'Very hot, dry spring — the hottest stretch before the rains begin.'),
        'summer': ('تابستان موسمی و پرباران با سرسبزی معابد آنکور.', 'Rainy monsoon summer, with Angkor\'s temples lush and green.'),
        'autumn': ('پاییز همچنان بارانی اما رو به کاهش در پایان فصل.', 'Autumn stays rainy but tapers off toward season\'s end.'),
        'winter': ('زمستان خنک‌تر و خشک، بهترین فصل برای بازدید از آنکور وات.', 'Cooler, dry winter — the best season to visit Angkor Wat.'),
    },
    'china': {
        'spring': ('بهار معتدل و پرگل در بیشتر مناطق، از هوای سرد شمال تا گرم جنوب.', 'Mild, blossoming spring across most regions, from cold in the north to warm in the south.'),
        'summer': ('تابستان گرم و مرطوب در جنوب و شرق، فصل باران در بسیاری از استان‌ها.', 'Hot, humid summer in the south and east, rainy season in many provinces.'),
        'autumn': ('پاییز خنک و آفتابی، محبوب‌ترین فصل برای گردشگری در چین.', 'Cool, sunny autumn — the most popular season for travel in China.'),
        'winter': ('زمستان سرد و خشک در شمال با برف فراوان، ملایم‌تر در جنوب.', 'Cold, dry winter with heavy snow in the north, milder in the south.'),
    },
    'cyprus': {
        'spring': ('بهار ملایم و پرگل با آسمانی صاف، فصل ایده‌آل گردش.', 'Mild, flowery spring with clear skies — an ideal season to explore.'),
        'summer': ('تابستان گرم و آفتابی مدیترانه‌ای، مناسب دریا و ساحل.', 'Hot, sunny Mediterranean summer — great for beaches and the sea.'),
        'autumn': ('پاییز گرم و آرام تا اواخر فصل، دریا همچنان قابل شنا.', 'Warm, calm autumn lasting late — the sea stays swimmable.'),
        'winter': ('زمستان ملایم و بارانی در سواحل، برف در کوهستان ترودوس.', 'Mild, rainy winter on the coast, snow in the Troodos mountains.'),
    },
    'georgia': {
        'spring': ('بهار سرسبز و بارانی، طبیعت قفقاز به‌سرعت شکوفا می‌شود.', 'Lush, rainy spring — the Caucasus landscape blooms quickly.'),
        'summer': ('تابستان گرم در دشت‌ها و خنک در کوهستان، فصل خوب کوهنوردی.', 'Warm in the lowlands and cool in the mountains — good hiking season.'),
        'autumn': ('پاییز طلایی، فصل برداشت انگور و بهترین زمان سفر به گرجستان.', 'Golden autumn, grape-harvest season and the best time to visit Georgia.'),
        'winter': ('زمستان سرد و برفی در کوهستان، مناسب اسکی در گودائوری.', 'Cold, snowy winter in the mountains — good skiing in Gudauri.'),
    },
    'india': {
        'spring': ('بهار گرم و خوشایند پیش از شروع گرمای شدید تابستان.', 'Warm, pleasant spring before the intense summer heat sets in.'),
        'summer': ('تابستان بسیار گرم در بیشتر مناطق و پرباران موسمی از ژوئن.', 'Very hot summer in most regions with monsoon rains from June.'),
        'autumn': ('پاییز رو به خنکی پس از پایان باران‌های موسمی.', 'Autumn cools down after the monsoon rains end.'),
        'winter': ('زمستان خنک و خوشایند در بیشتر نقاط، سرد در شمال کوهستانی.', 'Cool, pleasant winter in most areas, cold in the mountainous north.'),
    },
    'indonesia': {
        'spring': ('آب‌وهوای استوایی گرم با احتمال باران در تمام سال؛ بهار معمولاً کمی خشک‌تر.', 'Warm tropical climate with rain possible year-round; spring is usually a bit drier.'),
        'summer': ('فصل خشک با آفتاب فراوان، بهترین زمان برای جزایر و سواحل.', 'Dry season with plenty of sun — the best time for islands and beaches.'),
        'autumn': ('انتقال به فصل بارانی، رطوبت و بارش تدریجاً افزایش می‌یابد.', 'Transition into the rainy season, with humidity and rainfall gradually rising.'),
        'winter': ('فصل بارانی با رطوبت بالا و بارش‌های روزانه در بیشتر جزایر.', 'Rainy season with high humidity and daily showers across most islands.'),
    },
    'iran': {
        'spring': ('بهار معتدل و دلپذیر، فصل نوروز و بهترین زمان سفر در بیشتر مناطق.', 'Mild, pleasant spring — Nowruz season and the best travel time in most regions.'),
        'summer': ('تابستان گرم و خشک در فلات مرکزی، شرجی در سواحل خلیج فارس و خزر.', 'Hot, dry summer on the central plateau, humid along the Persian Gulf and Caspian coasts.'),
        'autumn': ('پاییز خنک و آفتابی، فصل زیبای رنگ پاییزی در شمال کشور.', 'Cool, sunny autumn — a beautiful season of fall colors in the north.'),
        'winter': ('زمستان سرد و برفی در ارتفاعات، ملایم‌تر در جنوب و سواحل.', 'Cold, snowy winter in the highlands, milder in the south and coasts.'),
    },
    'iraq': {
        'spring': ('بهار معتدل و خوشایند، بهترین فصل پیش از گرمای سوزان تابستان.', 'Mild, pleasant spring — the best season before summer\'s scorching heat.'),
        'summer': ('تابستان بسیار گرم و خشک با دمای بالای ۴۵ درجه در بسیاری از مناطق.', 'Very hot, dry summer with temperatures above 45°C in many areas.'),
        'autumn': ('پاییز رو به خنکی و مطبوع، مناسب گردش پس از پایان گرمای تابستان.', 'Autumn cools and becomes pleasant, good for sightseeing after summer heat.'),
        'winter': ('زمستان ملایم و بارانی، سرد و گاه برفی در مناطق کوهستانی شمال.', 'Mild, rainy winter; cold and occasionally snowy in the northern mountains.'),
    },
    'israel': {
        'spring': ('بهار معتدل و آفتابی، یکی از بهترین فصل‌های گردش.', 'Mild, sunny spring — one of the best seasons to explore.'),
        'summer': ('تابستان گرم و خشک، شرجی در سواحل مدیترانه‌ای.', 'Hot, dry summer, humid along the Mediterranean coast.'),
        'autumn': ('پاییز گرم و آرام تا اواخر فصل با کاهش تدریجی دما.', 'Warm, calm autumn lasting late with gradually cooling temperatures.'),
        'winter': ('زمستان ملایم و بارانی در سواحل، سرد در اورشلیم و ارتفاعات.', 'Mild, rainy winter on the coast, cold in Jerusalem and the highlands.'),
    },
    'japan': {
        'spring': ('بهار معتدل و رویایی با شکوفه‌های گیلاس (ساکورا)، محبوب‌ترین فصل سفر.', 'Mild, magical spring with cherry blossoms (sakura) — the most popular travel season.'),
        'summer': ('تابستان گرم و مرطوب با فصل باران در ژوئن و گرمای شدید در اوت.', 'Hot, humid summer with a rainy season in June and intense heat in August.'),
        'autumn': ('پاییز خنک با رنگ‌آمیزی زیبای برگ‌ها (کویو)، فصل دیگر محبوب گردشگری.', 'Cool autumn with beautiful fall foliage (koyo) — another beloved travel season.'),
        'winter': ('زمستان سرد و برفی در شمال و کوهستان، ملایم‌تر در جنوب.', 'Cold, snowy winter in the north and mountains, milder in the south.'),
    },
    'jordan': {
        'spring': ('بهار معتدل و دلپذیر با طبیعت سرسبز، بهترین فصل برای پترا و وادی رم.', 'Mild, pleasant spring with green landscapes — the best season for Petra and Wadi Rum.'),
        'summer': ('تابستان گرم و خشک، بسیار داغ در دره اردن و عقبه.', 'Hot, dry summer, very hot in the Jordan Valley and Aqaba.'),
        'autumn': ('پاییز آفتابی و معتدل، فصل دیگر خوب برای سفر.', 'Sunny, mild autumn — another good season for travel.'),
        'winter': ('زمستان خنک و بارانی، برف احتمالی در عمان و مناطق مرتفع.', 'Cool, rainy winter; possible snow in Amman and higher elevations.'),
    },
    'kazakhstan': {
        'spring': ('بهار متغیر با دمای رو به افزایش و طبیعت استپی سرسبز.', 'Variable spring with rising temperatures and green steppe landscapes.'),
        'summer': ('تابستان گرم و خشک در دشت‌های استپی، خنک‌تر در کوهستان‌های جنوب.', 'Hot, dry summer on the steppe, cooler in the southern mountains.'),
        'autumn': ('پاییز ملایم و کوتاه پیش از شروع سرمای زمستان.', 'Mild, short autumn before winter cold sets in.'),
        'winter': ('زمستان بسیار سرد با برف فراوان، به‌ویژه در آلماتی و شمال کشور.', 'Very cold winter with heavy snow, especially in Almaty and the north.'),
    },
    'kuwait': {
        'spring': ('بهار گرم و رو به داغی، فصل خوب پیش از تابستان سوزان.', 'Warm and warming spring — a good season before the scorching summer.'),
        'summer': ('تابستان بسیار داغ و خشک با دمای بالای ۴۵ درجه.', 'Extremely hot, dry summer with temperatures above 45°C.'),
        'autumn': ('پاییز رو به خنکی و قابل‌تحمل‌تر نسبت به تابستان.', 'Autumn cools and becomes more tolerable than summer.'),
        'winter': ('زمستان خنک و مطبوع، بهترین زمان بازدید از کویت.', 'Cool, pleasant winter — the best time to visit Kuwait.'),
    },
    'kyrgyzstan': {
        'spring': ('بهار سرسبز با آب شدن برف کوهستان تیان‌شان و مراتع پرگل.', 'Green spring as snow melts in the Tian Shan mountains, with flowering pastures.'),
        'summer': ('تابستان معتدل و خوشایند، بهترین فصل برای کوهنوردی و اسب‌سواری.', 'Mild, pleasant summer — the best season for trekking and horseback riding.'),
        'autumn': ('پاییز خنک با رنگ‌های طلایی در دره‌ها، فصل آرام‌تر گردشگری.', 'Cool autumn with golden colors in the valleys — a quieter travel season.'),
        'winter': ('زمستان سرد و برفی، مناسب اسکی در نزدیکی بیشکک.', 'Cold, snowy winter — good for skiing near Bishkek.'),
    },
    'laos': {
        'spring': ('بهار گرم و خشک، اوج گرما پیش از فصل باران.', 'Hot, dry spring — the hottest stretch before the rainy season.'),
        'summer': ('تابستان موسمی و پرباران با طبیعتی بسیار سرسبز.', 'Rainy monsoon summer with very lush landscapes.'),
        'autumn': ('پاییز همچنان تا حدی بارانی اما رو به خشک‌شدن.', 'Autumn still somewhat rainy but drying out.'),
        'winter': ('زمستان خنک و خشک، بهترین فصل برای سفر به لائوس.', 'Cool, dry winter — the best season to visit Laos.'),
    },
    'lebanon': {
        'spring': ('بهار معتدل و پرگل با برف باقی‌مانده روی قله‌های لبنان.', 'Mild, flowery spring with lingering snow on Lebanon\'s peaks.'),
        'summer': ('تابستان گرم و خشک در سواحل، خنک و مطبوع در کوهستان.', 'Hot, dry summer on the coast, cool and pleasant in the mountains.'),
        'autumn': ('پاییز آفتابی و ملایم، فصل خوب گردش در بیروت و کوهستان.', 'Sunny, mild autumn — a good season to explore Beirut and the mountains.'),
        'winter': ('زمستان بارانی در سواحل، برفی در کوهستان‌ها با پیست‌های اسکی.', 'Rainy winter on the coast, snowy in the mountains with ski resorts.'),
    },
    'malaysia': {
        'spring': ('آب‌وهوای استوایی گرم و مرطوب تقریباً ثابت در تمام سال.', 'Warm, humid equatorial climate that stays fairly constant year-round.'),
        'summer': ('گرم و شرجی با بارش‌های پراکنده بعدازظهر.', 'Hot and humid with scattered afternoon showers.'),
        'autumn': ('آغاز فصل بارانی‌تر در ساحل شرقی شبه‌جزیره مالزی.', 'Start of the wetter season on the east coast of Peninsular Malaysia.'),
        'winter': ('فصل موسمی شمال‌شرقی با بارش سنگین‌تر در ساحل شرقی.', 'Northeast monsoon season with heavier rain on the east coast.'),
    },
    'maldives': {
        'spring': ('گرم و آفتابی با دریایی آرام، پایان فصل خشک.', 'Warm and sunny with calm seas — the tail end of the dry season.'),
        'summer': ('آغاز موسمی جنوب‌غربی با احتمال باران و دریای متلاطم‌تر.', 'Start of the southwest monsoon with a chance of rain and choppier seas.'),
        'autumn': ('فصل مرطوب‌تر با بارش‌های گاه‌به‌گاه اما همچنان گرم.', 'Wetter season with occasional rain but still warm.'),
        'winter': ('فصل خشک و آفتابی، بهترین زمان برای غواصی و سفر به جزایر.', 'Dry, sunny season — the best time for diving and island travel.'),
    },
    'mongolia': {
        'spring': ('بهار خشک و بادخیز با دمای هنوز پایین در استپ‌های وسیع.', 'Dry, windy spring with still-cool temperatures across the vast steppe.'),
        'summer': ('تابستان کوتاه و معتدل، بهترین فصل برای سفر به مغولستان و صحرای گبی.', 'Short, mild summer — the best season to visit Mongolia and the Gobi Desert.'),
        'autumn': ('پاییز کوتاه و رو به سرما، دمای شب به‌سرعت کاهش می‌یابد.', 'Short autumn turning cold, with nighttime temperatures dropping fast.'),
        'winter': ('زمستان بسیار سرد و طولانی با دمای گاه زیر منفی ۳۰ درجه.', 'Very cold, long winter with temperatures sometimes below -30°C.'),
    },
    'myanmar': {
        'spring': ('بهار بسیار گرم و خشک، اوج گرما پیش از باران‌های موسمی.', 'Very hot, dry spring — the peak heat before the monsoon rains.'),
        'summer': ('تابستان موسمی و پرباران، معابد باگان در سبزی طبیعت.', 'Rainy monsoon summer, with Bagan\'s temples set in green surroundings.'),
        'autumn': ('پاییز رو به خشکی با کاهش تدریجی باران.', 'Autumn dries out with gradually decreasing rainfall.'),
        'winter': ('زمستان خنک و خشک، بهترین فصل برای بازدید از باگان و اینله.', 'Cool, dry winter — the best season to visit Bagan and Inle Lake.'),
    },
    'nepal': {
        'spring': ('بهار با شکوفایی رودودندرون و آسمان نسبتاً صاف، فصل خوب کوهنوردی.', 'Spring with blooming rhododendrons and fairly clear skies — a good trekking season.'),
        'summer': ('تابستان موسمی و پرباران، مسیرهای کوهستانی گاه گلی و ابری.', 'Rainy monsoon summer — mountain trails can be muddy and cloudy.'),
        'autumn': ('پاییز صاف و خنک با بهترین دید به هیمالیا؛ اوج فصل تراول و کوهنوردی.', 'Clear, crisp autumn with the best Himalayan views — peak trekking season.'),
        'winter': ('زمستان سرد در کوهستان و ملایم‌تر در کاتماندو و دره‌ها.', 'Cold in the mountains, milder in Kathmandu and the valleys.'),
    },
    'north-korea': {
        'spring': ('بهار معتدل با دمای رو به افزایش پس از زمستان سرد.', 'Mild spring with warming temperatures after a cold winter.'),
        'summer': ('تابستان گرم و مرطوب با بارش‌های موسمی در ژوئیه و اوت.', 'Warm, humid summer with monsoon rains in July and August.'),
        'autumn': ('پاییز خشک و آفتابی، فصل نسبتاً مطلوب برای گردش.', 'Dry, sunny autumn — a relatively favorable season to visit.'),
        'winter': ('زمستان بسیار سرد و خشک، به‌ویژه در مناطق شمالی.', 'Very cold, dry winter, especially in the northern regions.'),
    },
    'oman': {
        'spring': ('بهار گرم و رو به داغ‌شدن، هوای مطبوع در ارتفاعات جبل اخضر.', 'Warm and warming spring, with pleasant weather in the Jabal Akhdar highlands.'),
        'summer': ('تابستان بسیار داغ در بیشتر مناطق، اما ظفار تحت تأثیر موسمی خنک و مه‌آلود «خریف» است.', 'Very hot summer in most areas, but Dhofar enjoys the cool, misty "khareef" monsoon.'),
        'autumn': ('پاییز رو به خنکی، فصل خوبی برای بازدید از مسقط و کوهستان.', 'Autumn cools down — a good season to visit Muscat and the mountains.'),
        'winter': ('زمستان معتدل و دلپذیر، بهترین فصل سفر به عمان.', 'Mild, pleasant winter — the best season to travel to Oman.'),
    },
    'pakistan': {
        'spring': ('بهار معتدل در دشت‌ها، دلپذیر و پرگل در دره‌های شمالی مانند هونزا.', 'Mild in the plains, pleasant and flowery in northern valleys like Hunza.'),
        'summer': ('تابستان بسیار گرم در جنوب، خنک و مناسب کوهنوردی در شمال کوهستانی.', 'Very hot in the south, cool and great for trekking in the mountainous north.'),
        'autumn': ('پاییز خوشایند با رنگ‌های پاییزی زیبا در دره‌های شمالی.', 'Pleasant autumn with beautiful fall colors in the northern valleys.'),
        'winter': ('زمستان سرد و برفی در شمال، ملایم‌تر در دشت‌های جنوبی.', 'Cold, snowy winter in the north, milder on the southern plains.'),
    },
    'palestine': {
        'spring': ('بهار معتدل و سبز با گل‌های وحشی، فصل ایده‌آل سفر.', 'Mild, green spring with wildflowers — an ideal travel season.'),
        'summer': ('تابستان گرم و خشک، به‌ویژه در اریحا و دره اردن.', 'Hot, dry summer, especially in Jericho and the Jordan Valley.'),
        'autumn': ('پاییز آفتابی و ملایم تا اواخر فصل.', 'Sunny, mild autumn lasting into late in the season.'),
        'winter': ('زمستان خنک و بارانی، سرد و گاه برفی در بیت‌المقدس و رام‌الله.', 'Cool, rainy winter; cold and occasionally snowy in Jerusalem and Ramallah.'),
    },
    'philippines': {
        'spring': ('بهار گرم و خشک، اوج فصل آفتابی پیش از باران‌های تابستانی.', 'Hot, dry spring — the peak of the sunny season before summer rains.'),
        'summer': ('تابستان موسمی و پرباران، احتمال طوفان‌های استوایی افزایش می‌یابد.', 'Rainy monsoon summer, with an increased chance of tropical storms.'),
        'autumn': ('پاییز همچنان بارانی با احتمال تایفون در برخی مناطق.', 'Autumn remains rainy with a chance of typhoons in some areas.'),
        'winter': ('زمستان خنک‌تر و خشک، بهترین فصل برای سواحل و جزایر.', 'Cooler, drier season — the best time for beaches and islands.'),
    },
    'qatar': {
        'spring': ('بهار گرم و رو به داغی، مناسب گردش پیش از تابستان سوزان.', 'Warm, warming spring — good for sightseeing before the scorching summer.'),
        'summer': ('تابستان بسیار داغ و مرطوب با دمای بالای ۴۵ درجه.', 'Extremely hot, humid summer with temperatures above 45°C.'),
        'autumn': ('پاییز رو به خنکی و قابل‌تحمل‌تر برای فعالیت‌های بیرونی.', 'Autumn cools and becomes more tolerable for outdoor activities.'),
        'winter': ('زمستان معتدل و آفتابی، بهترین فصل بازدید از دوحه.', 'Mild, sunny winter — the best season to visit Doha.'),
    },
    'russia': {
        'spring': ('بهار سرد و کند در شمال، ملایم‌تر و سریع‌تر در جنوب.', 'Slow, cold spring in the north; milder and quicker in the south.'),
        'summer': ('تابستان معتدل و کوتاه، فصل شب‌های سفید در سن‌پترزبورگ.', 'Mild, short summer — the season of White Nights in Saint Petersburg.'),
        'autumn': ('پاییز کوتاه و رنگارنگ پیش از سرمای زودرس.', 'Short, colorful autumn before early cold sets in.'),
        'winter': ('زمستان طولانی و بسیار سرد با برف فراوان، به‌ویژه در سیبری.', 'Long, very cold winter with heavy snow, especially in Siberia.'),
    },
    'saudi-arabia': {
        'spring': ('بهار گرم و رو به داغی در بیشتر مناطق، ملایم‌تر در ارتفاعات عسیر.', 'Warm, warming spring in most areas, milder in the Asir highlands.'),
        'summer': ('تابستان بسیار داغ و خشک با دمای بالای ۴۵ درجه در بیشتر نقاط.', 'Very hot, dry summer with temperatures above 45°C in most areas.'),
        'autumn': ('پاییز رو به خنکی، فصل بهتر برای بازدید از ریاض و جده.', 'Autumn cools down — a better season to visit Riyadh and Jeddah.'),
        'winter': ('زمستان خنک و خوشایند، بهترین فصل برای سفر به عربستان.', 'Cool, pleasant winter — the best season to travel to Saudi Arabia.'),
    },
    'singapore': {
        'spring': ('آب‌وهوای استوایی گرم و مرطوب تقریباً ثابت در تمام سال با بارش‌های ناگهانی.', 'Warm, humid equatorial climate that stays fairly constant year-round, with sudden showers.'),
        'summer': ('گرم و شرجی با رطوبت بالا و بارش‌های کوتاه بعدازظهر.', 'Hot and humid with high humidity and brief afternoon showers.'),
        'autumn': ('همچنان گرم و مرطوب، بدون تغییر فصلی محسوس.', 'Still hot and humid, without much seasonal change.'),
        'winter': ('فصل موسمی شمال‌شرقی با بارش بیشتر در دسامبر و ژانویه.', 'Northeast monsoon season with more rain in December and January.'),
    },
    'south-korea': {
        'spring': ('بهار معتدل و زیبا با شکوفه‌های گیلاس، فصل محبوب گردشگری.', 'Mild, beautiful spring with cherry blossoms — a popular travel season.'),
        'summer': ('تابستان گرم و مرطوب با فصل باران موسمی «جانگما» در ژوئیه.', 'Hot, humid summer with the "jangma" monsoon rainy season in July.'),
        'autumn': ('پاییز خنک و آفتابی با رنگ‌های پاییزی خیره‌کننده، فصل محبوب دیگر.', 'Cool, sunny autumn with stunning fall foliage — another favorite season.'),
        'winter': ('زمستان سرد و گاه برفی، مناسب اسکی در پیونگ‌چانگ.', 'Cold, occasionally snowy winter — good for skiing in Pyeongchang.'),
    },
    'sri-lanka': {
        'spring': ('بهار گرم با احتمال باران بسته به منطقه، فصل خوب برای ساحل غربی.', 'Warm spring with rain chances varying by region — a good time for the west coast.'),
        'summer': ('موسمی جنوب‌غربی باران بیشتری به ساحل غرب و جنوب می‌آورد.', 'The southwest monsoon brings more rain to the west and south coasts.'),
        'autumn': ('انتقال بین دو موسمی، هوا متغیر و گاه بارانی است.', 'Transition between the two monsoons — weather is variable and sometimes rainy.'),
        'winter': ('موسمی شمال‌شرقی، ساحل شرقی بارانی‌تر و غرب خشک و آفتابی.', 'The northeast monsoon brings more rain to the east coast, while the west stays dry and sunny.'),
    },
    'syria': {
        'spring': ('بهار معتدل و سرسبز با گل‌های وحشی، بهترین فصل سفر.', 'Mild, green spring with wildflowers — the best travel season.'),
        'summer': ('تابستان گرم و خشک، بسیار داغ در مناطق داخلی و بیابانی.', 'Hot, dry summer, very hot in inland and desert areas.'),
        'autumn': ('پاییز آفتابی و ملایم با کاهش تدریجی دما.', 'Sunny, mild autumn with gradually cooling temperatures.'),
        'winter': ('زمستان خنک و بارانی در سواحل، سرد و گاه برفی در دمشق و ارتفاعات.', 'Cool, rainy winter on the coast; cold and occasionally snowy in Damascus and the highlands.'),
    },
    'taiwan': {
        'spring': ('بهار ملایم و کمی بارانی، فصل خوب پیش از گرمای تابستان.', 'Mild, slightly rainy spring — a good season before summer heat.'),
        'summer': ('تابستان گرم و مرطوب با احتمال تایفون از ژوئیه تا سپتامبر.', 'Hot, humid summer with a chance of typhoons from July to September.'),
        'autumn': ('پاییز خوشایند و کمتر بارانی، فصل مناسب کوهنوردی.', 'Pleasant, less rainy autumn — a good season for hiking.'),
        'winter': ('زمستان ملایم و مرطوب در شمال، معتدل‌تر و آفتابی‌تر در جنوب.', 'Mild, damp winter in the north, milder and sunnier in the south.'),
    },
    'tajikistan': {
        'spring': ('بهار سرسبز با آب شدن برف کوهستان پامیر، فصل خوب برای دره‌های سبز.', 'Green spring as Pamir mountain snow melts — a good season for lush valleys.'),
        'summer': ('تابستان گرم در دوشنبه، خنک و مناسب کوهنوردی در ارتفاعات پامیر.', 'Warm in Dushanbe, cool and great for trekking in the Pamir highlands.'),
        'autumn': ('پاییز خنک با رنگ‌های زیبا در دره‌ها، فصل آرام گردشگری.', 'Cool autumn with beautiful colors in the valleys — a quiet travel season.'),
        'winter': ('زمستان سرد و برفی، به‌ویژه در مناطق کوهستانی مرتفع.', 'Cold, snowy winter, especially in the high mountain regions.'),
    },
    'thailand': {
        'spring': ('بهار بسیار گرم، اوج گرما پیش از باران‌های موسمی.', 'Very hot spring — the peak heat before the monsoon rains.'),
        'summer': ('تابستان موسمی و پرباران با طبیعتی سرسبز.', 'Rainy monsoon summer with lush green landscapes.'),
        'autumn': ('پاییز همچنان تا حدی بارانی، رو به خشک‌شدن در پایان فصل.', 'Autumn stays somewhat rainy, drying out toward the end of the season.'),
        'winter': ('زمستان خنک و خشک، بهترین فصل برای سفر به تایلند.', 'Cool, dry winter — the best season to visit Thailand.'),
    },
    'timor-leste': {
        'spring': ('گرم و رو به خشک‌شدن، پایان فصل بارانی.', 'Warm and drying out — the tail end of the rainy season.'),
        'summer': ('فصل خشک و آفتابی، مناسب گردش و غواصی.', 'Dry, sunny season — good for sightseeing and diving.'),
        'autumn': ('همچنان خشک با دمای بالا، رو به شروع دوباره باران.', 'Still dry with high temperatures, approaching the return of the rains.'),
        'winter': ('فصل بارانی گرم و مرطوب.', 'Warm, humid rainy season.'),
    },
    'turkey': {
        'spring': ('بهار معتدل و پرگل، فصل ایده‌آل برای استانبول و کاپادوکیه.', 'Mild, flowery spring — an ideal season for Istanbul and Cappadocia.'),
        'summer': ('تابستان گرم و خشک در سواحل اژه و مدیترانه، معتدل‌تر در آنکارا.', 'Hot, dry summer on the Aegean and Mediterranean coasts, milder in Ankara.'),
        'autumn': ('پاییز آفتابی و ملایم، فصل دیگر محبوب برای سفر.', 'Sunny, mild autumn — another popular travel season.'),
        'winter': ('زمستان سرد و برفی در آناتولی مرکزی، ملایم‌تر و بارانی در سواحل.', 'Cold, snowy winter in central Anatolia, milder and rainy along the coasts.'),
    },
    'turkmenistan': {
        'spring': ('بهار ملایم و کوتاه، بهترین فصل پیش از گرمای بیابانی تابستان.', 'Mild, short spring — the best season before the desert summer heat.'),
        'summer': ('تابستان بسیار داغ و خشک در بیابان قره‌قوم.', 'Very hot, dry summer across the Karakum Desert.'),
        'autumn': ('پاییز خوشایند و آفتابی، فصل مناسب دیگر برای سفر.', 'Pleasant, sunny autumn — another good travel season.'),
        'winter': ('زمستان سرد و گاه برفی، به‌ویژه در شب‌های بیابانی.', 'Cold, occasionally snowy winter, especially on desert nights.'),
    },
    'united-arab-emirates': {
        'spring': ('بهار گرم و آفتابی، فصل خوب گردش پیش از تابستان سوزان.', 'Warm, sunny spring — a good season to explore before the scorching summer.'),
        'summer': ('تابستان بسیار داغ و مرطوب با دمای بالای ۴۵ درجه.', 'Extremely hot, humid summer with temperatures above 45°C.'),
        'autumn': ('پاییز رو به خنکی، مناسب فعالیت‌های بیرونی از اواخر فصل.', 'Autumn cools down, good for outdoor activities from late season.'),
        'winter': ('زمستان معتدل و آفتابی، بهترین فصل سفر به دبی و ابوظبی.', 'Mild, sunny winter — the best season to visit Dubai and Abu Dhabi.'),
    },
    'uzbekistan': {
        'spring': ('بهار ملایم و سرسبز، بهترین فصل برای بازدید از سمرقند و بخارا.', 'Mild, green spring — the best season to visit Samarkand and Bukhara.'),
        'summer': ('تابستان بسیار گرم و خشک در سراسر کشور.', 'Very hot, dry summer throughout the country.'),
        'autumn': ('پاییز آفتابی و خوشایند، فصل دیگر مناسب گردشگری.', 'Sunny, pleasant autumn — another good travel season.'),
        'winter': ('زمستان سرد و گاه برفی، به‌ویژه در تاشکند.', 'Cold, occasionally snowy winter, especially in Tashkent.'),
    },
    'vietnam': {
        'spring': ('بهار ملایم در شمال، گرم و خشک در جنوب.', 'Mild in the north, warm and dry in the south.'),
        'summer': ('تابستان گرم و مرطوب با باران‌های موسمی، به‌ویژه در شمال و مرکز.', 'Hot, humid summer with monsoon rains, especially in the north and center.'),
        'autumn': ('پاییز خوشایند در شمال، فصل احتمال طوفان در سواحل مرکزی.', 'Pleasant autumn in the north — a season with typhoon risk on the central coast.'),
        'winter': ('زمستان خنک و مه‌آلود در شمال، گرم و آفتابی در جنوب.', 'Cool, misty winter in the north, warm and sunny in the south.'),
    },
    'yemen': {
        'spring': ('بهار گرم در سواحل، ملایم‌تر و دلپذیر در ارتفاعات صنعا.', 'Warm on the coasts, milder and pleasant in the Sana\'a highlands.'),
        'summer': ('تابستان بسیار داغ در سواحل، معتدل‌تر در کوهستان‌های مرتفع.', 'Very hot on the coasts, milder in the high mountains.'),
        'autumn': ('پاییز رو به خنکی در ارتفاعات، همچنان گرم در سواحل.', 'Autumn cools in the highlands, while coasts remain warm.'),
        'winter': ('زمستان خنک و گاه سرد در ارتفاعات، ملایم در سواحل جنوبی.', 'Cool, sometimes cold winter in the highlands, mild on the southern coasts.'),
    },
}


def seed_weather(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    for slug, seasons in WEATHER.items():
        try:
            country = Country.objects.get(slug=slug)
        except Country.DoesNotExist:
            continue
        for season, (fa, en) in seasons.items():
            setattr(country, f'weather_{season}_fa', fa)
            setattr(country, f'weather_{season}_en', en)
        country.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_country_weather_fields'),
    ]

    operations = [
        migrations.RunPython(seed_weather, noop),
    ]
