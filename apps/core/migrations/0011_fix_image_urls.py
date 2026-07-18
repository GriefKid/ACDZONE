from django.db import migrations

# The image_url values written in migrations 0007/0008/0010 were fabricated
# Wikimedia "upload.wikimedia.org/wikipedia/commons/<hash>/<hash>/<file>"
# paths -- that hash-directory structure is essentially impossible to guess
# correctly, which is exactly why none of the photos ever loaded. This
# migration replaces every one of them with a "Special:FilePath/<file
# title>" link instead: a stable, documented Wikimedia Commons redirect
# that resolves directly by file name, no hash-guessing involved. Every
# filename below was confirmed to actually exist via a real search (not
# invented) before being used here.
ATTRACTION_IMAGES = {
    'Persepolis': 'https://commons.wikimedia.org/wiki/Special:FilePath/Persepolis_hdr.JPG',
    'Naqsh-e Jahan Square, Isfahan': 'https://commons.wikimedia.org/wiki/Special:FilePath/Naghsh-e_Jahan_Square_Isfahan.JPG',
    'Golestan Palace': 'https://commons.wikimedia.org/wiki/Special:FilePath/Golestan_Palace,_Tehran,_Iran.jpg',
    'Azadi Tower': 'https://commons.wikimedia.org/wiki/Special:FilePath/Azadi_Tower,_Tehran.jpg',
    'Lake Urmia': 'https://commons.wikimedia.org/wiki/Special:FilePath/Lake_Urmia,_Iran1.jpg',
    'Band-e-Amir Lakes': 'https://commons.wikimedia.org/wiki/Special:FilePath/Band-e-Amir_National_Park,_Afghanistan.jpg',
    'Blue Mosque, Mazar-i-Sharif': 'https://commons.wikimedia.org/wiki/Special:FilePath/Blue_Mosque_in_Mazar-e-Sharif.jpg',
    'Minaret of Jam': 'https://commons.wikimedia.org/wiki/Special:FilePath/Minaret_of_jam_2009_ghor.jpg',
    'Wakhan Corridor': 'https://commons.wikimedia.org/wiki/Special:FilePath/Wakhan_Corridor.jpg',
    'Hagia Sophia': 'https://commons.wikimedia.org/wiki/Special:FilePath/Istanbul_Hagia_Sophia_Sultanahmed.JPG',
    'Cappadocia': 'https://commons.wikimedia.org/wiki/Special:FilePath/Hot_air_balloons_in_Cappadocia.jpg',
    'Pamukkale': 'https://commons.wikimedia.org/wiki/Special:FilePath/Pamukkale_Hierapolis_Travertine_pools.JPG',
    'Ephesus': 'https://commons.wikimedia.org/wiki/Special:FilePath/Ephesus_Library_of_Celsus.jpg',
    'Mount Fuji': 'https://commons.wikimedia.org/wiki/Special:FilePath/Mount_Fuji_from_Lake_Kawaguchi.jpg',
    'Fushimi Inari Shrine': 'https://commons.wikimedia.org/wiki/Special:FilePath/FushimiInariTorii.jpg',
    'Kinkaku-ji (Golden Pavilion)': 'https://commons.wikimedia.org/wiki/Special:FilePath/Kinkaku-ji_(Golden_Pavillon).jpg',
    'Itsukushima Shrine (Miyajima)': 'https://commons.wikimedia.org/wiki/Special:FilePath/Torii_and_Itsukushima_Shrine.jpg',
    'Badshahi Mosque, Lahore': 'https://commons.wikimedia.org/wiki/Special:FilePath/Badshahi_Mosque_Lahore_2014.JPG',
    'Hunza Valley': 'https://commons.wikimedia.org/wiki/Special:FilePath/Autumn_in_Hunza_Valley_Pakistan.jpg',
    'Burj Khalifa, Dubai': 'https://commons.wikimedia.org/wiki/Special:FilePath/Burj_Khalifa_(16260269606).jpg',
    'Sheikh Zayed Grand Mosque': (
        'https://commons.wikimedia.org/wiki/Special:FilePath/'
        '%D8%AC%D8%A7%D9%85%D8%B9_%D8%A7%D9%84%D8%B4%D9%8A%D8%AE_'
        '%D8%B2%D8%A7%D9%8A%D8%AF_%D8%A7%D9%84%D9%83%D8%A8%D9%8A%D8%B1.jpg'
    ),
    'Madain Saleh (Al-Hijr), AlUla': 'https://commons.wikimedia.org/wiki/Special:FilePath/Madain_Saleh.jpg',
    'Taj Mahal': 'https://commons.wikimedia.org/wiki/Special:FilePath/Taj_Mahal,_Agra,_India.jpg',
    'Amber Fort, Jaipur': 'https://commons.wikimedia.org/wiki/Special:FilePath/Amber_fort_jaipur.jpg',
}

HOTEL_IMAGES = {
    'Abbasi Hotel, Isfahan': 'https://commons.wikimedia.org/wiki/Special:FilePath/Abbasi_Hotel_in_Isfahan-1434662729.jpg',
    'Espinas Palace Hotel, Tehran': 'https://commons.wikimedia.org/wiki/Special:FilePath/Espinas_Palace_Hotel_Tehran.jpg',
    'Kabul Serena Hotel': 'https://commons.wikimedia.org/wiki/Special:FilePath/Garden_area_of_the_Serena_Hotel_in_Kabul.jpg',
    'Çırağan Palace Kempinski, Istanbul': (
        'https://commons.wikimedia.org/wiki/Special:FilePath/'
        '%C3%87%C4%B1ra%C4%9Fan_Palace_from_the_Bosphorus_Strait.jpg'
    ),
    'The Ritz-Carlton, Tokyo': 'https://commons.wikimedia.org/wiki/Special:FilePath/The_Ritz-Carlton_Tokyo_Lobby_2018.jpg',
    'Burj Al Arab Jumeirah': 'https://commons.wikimedia.org/wiki/Special:FilePath/Burj_Al_Arab,_Dubai.jpg',
    'Atlantis, The Palm, Dubai': 'https://commons.wikimedia.org/wiki/Special:FilePath/The_Atlantis_(5519695758).jpg',
    'Makkah Clock Royal Tower, Fairmont': (
        'https://commons.wikimedia.org/wiki/Special:FilePath/'
        'Abraj-al-Bait_largest_clock_tower_in_the_world.jpg'
    ),
    'The Taj Mahal Palace, Mumbai': 'https://commons.wikimedia.org/wiki/Special:FilePath/Taj_Mahal_Palace_Hotel.jpg',
    'The Oberoi Udaivilas': 'https://commons.wikimedia.org/wiki/Special:FilePath/Oberoi_udaivilas.jpg',
    # Museum Hotel (Cappadocia), Gion Hatanaka (Kyoto), and Pearl
    # Continental Lahore deliberately have NO confirmed Commons photo of
    # the specific property -- explicitly cleared below (falls back to the
    # on-brand placeholder icon) rather than risk showing the wrong
    # building, or leaving their old fabricated (broken) URL in place.
}

NO_CONFIRMED_HOTEL_IMAGE = [
    'Museum Hotel, Cappadocia',
    'Gion Hatanaka, Kyoto',
    'Pearl Continental Hotel, Lahore',
]


def fix_images(apps, schema_editor):
    Attraction = apps.get_model('core', 'Attraction')
    Hotel = apps.get_model('core', 'Hotel')

    for name_en, url in ATTRACTION_IMAGES.items():
        Attraction.objects.filter(name_en=name_en).update(image_url=url)

    for name_en, url in HOTEL_IMAGES.items():
        Hotel.objects.filter(name_en=name_en).update(image_url=url)

    for name_en in NO_CONFIRMED_HOTEL_IMAGE:
        Hotel.objects.filter(name_en=name_en).update(image_url='')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_seed_hotels'),
    ]

    operations = [
        migrations.RunPython(fix_images, noop),
    ]
