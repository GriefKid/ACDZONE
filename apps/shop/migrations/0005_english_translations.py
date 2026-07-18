from django.db import migrations

# English side of the product/category content seeded in 0003/0004. Until
# now only the _fa columns were set, so switching the site to English fell
# back to the Persian text (MODELTRANSLATION_FALLBACK_LANGUAGES = ('fa',
# 'en')) instead of actually translating — this migration fixes that.
# Editable from /admin/ afterwards like any other field.

CATEGORY_NAMES_EN = {
    'کارت‌های شارژ بین‌المللی': 'International Charge Cards',
    'بلیط بالن‌سواری': 'Hot Air Balloon Ride Tickets',
}

# Short descriptions for VisaCard/Ab Sard/Ahmadabad reuse the exact English
# sentences already vetted in apps/core/translations.py (written for the
# home carousel captions) — same product, same wording, one source of truth
# in spirit even though these live in the DB instead of that dict.
PRODUCT_EN = {
    'یونیون‌کارت': {
        'title_en': 'UnionCard',
        'description_en': (
            "After all these years, it's time to free your new experiences "
            "from the stone curse of sanctions and restrictions. Get your "
            "UnionPay card today and shop freely across the international "
            "market, transferring money without limits."
        ),
        'long_description_en': (
            "The miracle that frees us from the stone curse of sanctions "
            "has finally arrived in Iran, and it's exactly here: "
            "UnionPay.\n\n"
            "You no longer need to buy AI subscriptions like ChatGPT or "
            "Claude through unreliable sites with sky-high fees, or wait "
            "days to transfer money across the world while worrying about "
            "untrustworthy middlemen.\n\n"
            "With UnionPay cards and payment network, you can easily "
            "subscribe to any AI service on your own, buy any product or "
            "software you want from international sites, and transfer "
            "money anywhere in the world within minutes, worry-free. The "
            "UnionPay international card and payment network is the one "
            "true way to make all of this possible.\n\n"
            "UnionPay Features & Technical Specifications — Getting to "
            "Know the World's Largest Payment Network\n"
            "Today, electronic payments are an inseparable part of daily "
            "life. From online shopping to paying hotel bills, booking "
            "flights, or withdrawing cash from ATMs, all of this is made "
            "possible thanks to international payment networks. Alongside "
            "well-known names like Visa and Mastercard, UnionPay stands as "
            "one of the largest and most powerful payment networks in the "
            "world.\n\n"
            "Founded in China in 2002, UnionPay today supports billions of "
            "bank cards worldwide. The network is not only the backbone of "
            "electronic payments in China, but has also significantly "
            "expanded its presence in international markets in recent "
            "years.\n\n"
            "Global Coverage: From China to Over 174 Countries\n"
            "One of UnionPay's biggest advantages is the sheer size of its "
            "acceptance network. Today, UnionPay cards can be used in more "
            "than 174 countries and regions, with millions of stores, "
            "ATMs, hotels, restaurants, websites, and online shops "
            "supporting the network.\n\n"
            "Payment Technologies at UnionPay\n"
            "One of UnionPay's key strengths is its use of the latest "
            "global technologies to increase the speed, security, and "
            "convenience of payments.\n"
            "EMV smart chip: Nearly all new UnionPay cards come equipped "
            "with an EMV smart chip. Unlike older cards that stored data "
            "on a magnetic stripe, this chip generates a unique encrypted "
            "code for every transaction, significantly reducing the risk "
            "of card cloning or misuse of banking information.\n"
            "Mobile payments: UnionPay also allows bank cards to be linked "
            "to digital wallets and mobile apps, letting users shop or pay "
            "for services with just their phone, no physical card "
            "required.\n"
            "QR code payments: users can complete a payment in seconds "
            "just by scanning a QR code; thanks to its speed and low cost, "
            "this has become one of the most popular payment methods "
            "across Asia.\n\n"
            "UnionPay Network Security\n"
            "One of the main reasons users trust UnionPay is its high "
            "level of security: advanced card-data encryption, "
            "tokenization technology to hide the real card number, "
            "multi-factor authentication for online payments, dynamic or "
            "one-time passcodes, smart systems that detect suspicious "
            "transactions, and real-time transaction monitoring to "
            "prevent fraud — together, these technologies put UnionPay's "
            "security on par with the world's other major networks.\n\n"
            "Support for International Payments\n"
            "Although UnionPay is a Chinese payment network, it is now "
            "fully optimized for international transactions as well; it "
            "supports the US dollar, euro, British pound, Chinese yuan, "
            "and dozens of other currencies, automatically converting and "
            "settling the amount whenever you make a purchase abroad. "
            "This is exactly why many students, traders, tourists, and "
            "companies working with the Chinese market choose UnionPay.\n\n"
            "Cash Withdrawals from International ATMs\n"
            "In addition to in-person and online purchases, UnionPay "
            "cardholders can withdraw cash from millions of ATMs across "
            "different countries; daily withdrawal limits, fees, and "
            "per-transaction restrictions depend on the rules of the "
            "issuing and acquiring banks.\n\n"
            "Benefits of Using UnionPay\n"
            "Extremely wide coverage across China; usable in more than "
            "180 countries worldwide; high security with the latest "
            "encryption technologies; contactless (NFC) payment support; "
            "QR code payment option; compatibility with digital wallets; "
            "fast transaction processing; competitive fees for banks and "
            "merchants; and well-suited for international travel and "
            "trade.\n\n"
            "Who Is a UnionPay Card Right For?\n"
            "This card wasn't designed for everyone, but for some people "
            "it's one of the best options for everyday and international "
            "payments — especially if your financial activity connects to "
            "China or other Asian countries:\n"
            "People traveling to Asian countries for leisure, work, or to "
            "visit family — the card is accepted at most stores, "
            "restaurants, hotels, malls, and ATMs across Asia, reducing "
            "the need to carry cash.\n"
            "Students studying in China who deal daily with tuition, "
            "dormitory costs, food, and transportation.\n"
            "Merchants and business people working with Asian companies "
            "and suppliers.\n"
            "Tourists and travelers visiting China, Hong Kong, Singapore, "
            "Malaysia, Thailand, and other Asian countries.\n"
            "Anyone making international online purchases (it's best to "
            "check beforehand whether the store in question supports "
            "this network).\n"
            "Anyone for whom payment security is the top priority.\n"
            "Anyone connected to the Chinese market: importers, "
            "exporters, merchants, shipping companies, students, and "
            "researchers.\n\n"
            "Is a UnionPay Card Right for Everyone?\n"
            "Despite its many advantages, it isn't the best choice for "
            "everyone. If most of your payments happen in countries where "
            "the network's acceptance is more limited, or you have no "
            "connection to China or Asian markets, other payment networks "
            "might suit you better.\n\n"
            "Summary\n"
            "Above all, the UnionPay card suits people who travel to Asia "
            "— especially East Asian countries — live or study there, "
            "work with Chinese companies, or regularly make international "
            "payments. Wide acceptance across China, strong security, "
            "both in-person and online payments, and access to financial "
            "services in many countries around the world make this card "
            "a practical choice for international users."
        ),
    },
    'ویزاکارت': {
        'title_en': 'VisaCard',
        'description_en': 'The international Visa charge card, accepted at most online stores worldwide.',
    },
    'بالن‌سواری آب‌سرد': {
        'title_en': 'Ab Sard Balloon Ride',
        'description_en': 'A hot air balloon flight experience over the Ab Sard region.',
    },
    'بالن‌سواری احمدآباد مستوفی': {
        'title_en': 'Ahmadabad Mostofi Balloon Ride',
        'description_en': 'A hot air balloon flight experience over Ahmadabad Mostofi.',
    },
}


def add_english_translations(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Product = apps.get_model('shop', 'Product')

    for name_fa, name_en in CATEGORY_NAMES_EN.items():
        Category.objects.filter(name_fa=name_fa).update(name_en=name_en)

    for title_fa, fields in PRODUCT_EN.items():
        Product.objects.filter(title_fa=title_fa).update(**fields)


def remove_english_translations(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Product = apps.get_model('shop', 'Product')

    Category.objects.filter(name_fa__in=CATEGORY_NAMES_EN.keys()).update(name_en=None)
    Product.objects.filter(title_fa__in=PRODUCT_EN.keys()).update(
        title_en=None, description_en=None, long_description_en=None,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_seed_remaining_products'),
    ]

    operations = [
        migrations.RunPython(add_english_translations, remove_english_translations),
    ]
