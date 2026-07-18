"""
Hand-maintained Persian -> English translation table.

Normally, UI text in Django goes through the standard {% trans %} /
gettext_lazy() pipeline: `django-admin makemessages -l en` scans the
codebase and generates locale/en/LC_MESSAGES/django.po, a translator
fills in the English text, then `compilemessages` compiles it to a
binary .mo file that Django actually loads at runtime.

Both of those commands need the GNU gettext command-line tools
installed, and this dev environment doesn't have them available (see
README, "نکته درباره‌ی ترجمه‌ی متن‌های ثابت"). Rather than block on
that, this module IS the English translation, looked up directly at
render time:

  - templates use {% t "فارسی" %} (apps/core/templatetags/acd_i18n.py)
    instead of {% trans "فارسی" %}
  - Python code that needs the same behaviour imports `translate()`
    directly (see apps/accounts/forms.py)

Add every Persian source string used anywhere on the public site as a
key here, with its English text as the value. If English is active and
a string isn't found here, the Persian source is shown as a fallback
(better than a crash, and easy to spot while translating incrementally).

Once gettext is installed, this whole module can be retired: swap
{% t %} back for {% trans %}, run makemessages -l en, paste these same
translations into the generated .po file, run compilemessages, done.
"""
from django.utils.functional import lazy
from django.utils.translation import get_language

TRANSLATIONS = {
    # Header / nav
    'خانه': 'Home',
    'داشبورد': 'Dashboard',
    'کشورها': 'Countries',
    'نماینده‌ها': 'Representatives',
    'نماینده‌ای ثبت نشده است.': 'No representative has been added yet.',
    'لیست کشورها از پنل ادمین مدیریت می‌شود (به‌زودی)': 'The list of countries is managed from the admin panel (coming soon)',
    'پروفایل': 'Profile',
    'محصولات من': 'My Products',
    'خروج': 'Log out',
    'ورود': 'Log in',
    'عضویت': 'Sign up',

    # Notification bell (header, all pages)
    'پیش': 'ago',
    'اعلانی وجود ندارد': 'No notifications',
    'علامت‌گذاری همه به‌عنوان خوانده‌شده': 'Mark all as read',

    # Country pages (apps/core/models.py Country — header dropdown +
    # templates/core/country_detail.html). name/description are
    # modeltranslation DB fields (name_fa/name_en, description_fa/
    # description_en), same as Product/Post — read directly in templates,
    # not through {% t %}. Only the page's own static strings are needed
    # here.
    'سرود ملی': 'National Anthem',
    'مرورگر شما از پخش این فایل صوتی پشتیبانی نمی‌کند.': 'Your browser does not support playing this audio file.',
    'توضیحاتی برای این کشور ثبت نشده است.': 'No description has been added for this country yet.',

    # Representative pages
    'نماینده رسمی': 'Official representative',
    'اطلاعات تماس': 'Contact information',
    'کشور نمایندگی': 'Representative country',
    'پروفایل نماینده': 'Representative profile',
    'اطلاعات تکمیلی این نماینده هنوز ثبت نشده است.': 'Additional information for this representative has not been added yet.',
    'فارسی': 'Persian',

    # Footer
    'کارت‌های شارژ بین‌المللی و تجربه‌ی بالن‌سواری — با اطمینان و امنیت کامل.':
        'International charge cards and hot air balloon experiences — with full trust and security.',
    'تلگرام': 'Telegram',
    'واتساپ': 'WhatsApp',
    'تماس با ما': 'Contact us',
    'قوانین و مقررات': 'Terms & conditions',

    # Home
    'به ACD Zone خوش آمدید': 'Welcome to ACD Zone',
    'مقصد شما برای خرید کارت‌های شارژ بین‌المللی و تجربه‌ی بالن‌سواری‌های فراموش‌نشدنی.':
        'Your destination for international charge cards and unforgettable hot air balloon experiences.',
    'مشاهده محصولات': 'View products',
    'مرورگر شما از پخش این ویدیو پشتیبانی نمی‌کند.': 'Your browser does not support playing this video.',
    'ویدیو یا تصویر معرفی سایت (از پنل ادمین قابل مدیریت خواهد بود)':
        'Site introduction video or image (will be manageable from the admin panel)',
    'محصولات ما': 'Our products',
    'تصویر محصول به‌زودی': 'Product image coming soon',
    'مشاهده': 'View',
    'قبلی': 'Previous',
    'بعدی': 'Next',
    'آخرین مطالب': 'Latest posts',
    'به محض انتشار اولین پست در ACDNews و ACDNotes، خلاصه‌ی آن‌ها همراه با لینک به همان صفحه اینجا نمایش داده می‌شود.':
        "As soon as the first post is published on ACDNews or ACDNotes, a summary with a link to it will appear here.",

    # Products — NOTE: product.title/description/long_description are
    # modeltranslation DB fields now (apps/shop/models.py), read directly
    # in templates (not through {% t %}), so the entries below are NOT
    # actually consulted for them anymore and are kept only because they
    # still happen to match, as a quick human cross-reference. The real,
    # live English text lives in the database itself (title_en/
    # description_en/long_description_en columns), seeded by
    # apps/shop/migrations/0005_english_translations.py and editable from
    # /admin/ — edit it there, not here.
    'یونیون‌کارت': 'UnionCard',
    'ویزاکارت': 'VisaCard',
    'بالن‌سواری آب‌سرد': 'Ab Sard Balloon Ride',
    'بالن‌سواری احمدآباد مستوفی': 'Ahmadabad Mostofi Balloon Ride',
    'کارت شارژ بین‌المللی یونیون‌کارت، برای خریدهای آنلاین و بین‌المللی.':
        'The UnionCard international charge card, for online and international purchases.',
    'کارت شارژ بین‌المللی ویزا، پذیرفته‌شده در اکثر فروشگاه‌های آنلاین دنیا.':
        'The international Visa charge card, accepted at most online stores worldwide.',
    'تجربه‌ی پرواز با بالن بر فراز منطقه‌ی آب‌سرد.': 'A hot air balloon flight experience over the Ab Sard region.',
    'تجربه‌ی پرواز با بالن بر فراز احمدآباد مستوفی.': 'A hot air balloon flight experience over Ahmadabad Mostofi.',

    # ACDPay
    'خرید امن کارت‌های شارژ بین‌المللی': 'Secure purchase of international charge cards',
    'ضمانت اصالت کالا': 'Authenticity guaranteed',
    'پرداخت امن': 'Secure payment',
    'پیگیری سفارش': 'Order tracking',
    'پشتیبانی ۲۴ ساعته': '24/7 support',
    'اطلاع‌رسانی پیامکی': 'SMS notifications',
    'توضیحات و مبلغ محصول از پنل ادمین تنظیم می‌شود.': 'Product description and price are set from the admin panel.',
    'خرید (به‌زودی فعال می‌شود)': 'Buy (coming soon)',
    'خرید': 'Buy',
    'تومان': 'Toman',
    'به‌زودی محصولی برای نمایش اضافه می‌شود.': 'Products will be added here soon.',
    'ویدیوی معرفی کارت‌ها': 'Card introduction video',
    'این کارت‌ها چطور کار می‌کنند؟': 'How do these cards work?',
    'متن معرفی و راهنمای استفاده از کارت‌ها اینجا نمایش داده می‌شود؛ این محتوا هم از پنل ادمین قابل ویرایش خواهد بود.':
        'An introduction and usage guide for the cards will appear here; this content will also be editable from the admin panel.',

    # Welcome mascot (templates/partials/welcome_mascot.html)
    'سلام! رو دکمه‌ی «داشبورد» بزن تا همه‌ی خدمات ما رو یک‌جا ببینی.':
        'Hi there! Tap "Dashboard" to see all our services in one place.',
    'برو داشبورد': 'Go to dashboard',
    'ببر همراه ACD Zone': 'The ACD Zone companion tiger cub',

    # Auth-required modal (templates/partials/auth_required_modal.html)
    'برای خرید، ابتدا وارد شوید': 'Please sign in to continue',
    'برای ثبت سفارش و پیگیری آن در «محصولات من»، باید وارد حساب کاربری‌تان شوید.':
        'To place an order and track it under "My Products", please sign in to your account first.',
    'ورود به حساب': 'Sign in',
    'حساب کاربری ندارید؟ عضو شوید': "Don't have an account? Sign up",
    'بستن': 'Close',

    # ACDBallons
    'خرید بلیط بالن‌سواری': 'Buy hot air balloon ride tickets',
    'ضمانت رزرو': 'Booking guaranteed',
    'توضیحات و مبلغ بلیط از پنل ادمین تنظیم می‌شود.': 'Ticket description and price are set from the admin panel.',
    'به‌زودی بلیطی برای نمایش اضافه می‌شود.': 'Tickets will be added here soon.',
    'ویدیوی معرفی بالن‌سواری‌ها': 'Balloon ride introduction video',
    'تجربه‌ی بالن‌سواری چگونه است؟': 'What is the hot air balloon experience like?',
    'متن معرفی، مسیر و زمان‌بندی پروازها اینجا نمایش داده می‌شود؛ این محتوا هم از پنل ادمین قابل ویرایش خواهد بود.':
        'Route and flight schedule details will appear here; this content will also be editable from the admin panel.',

    # Buy flow (apps/shop/forms.py, templates/shop/buy.html)
    'نام و نام خانوادگی': 'Full name',
    'شماره واتساپ/تلگرام/بله': 'WhatsApp/Telegram/Bale number',
    'ثبت درخواست خرید': 'Submit purchase request',
    'این فرم فقط درخواست خرید را ثبت می‌کند؛ راهنمای پرداخت را همکاران ما برایتان ارسال می‌کنند.':
        'This form only submits the purchase request; our team will send you payment instructions afterwards.',
    'درخواست خرید شما ثبت شد؛ همکاران ما به‌زودی پیگیری می‌کنند.':
        'Your purchase request has been submitted; our team will follow up soon.',

    # Order detail (templates/shop/order_detail.html)
    'جزئیات سفارش': 'Order details',
    'بازگشت به محصولات من': 'Back to My Products',
    'شماره سفارش': 'Order number',
    'تاریخ ثبت': 'Submitted on',
    'مرحله‌ی سفارش': 'Order progress',
    'مشاهده جزئیات': 'View details',
    'حذف': 'Delete',
    'محصول از لیست حذف شد.': 'Removed from your list.',

    # Dashboard
    'خرید کارت‌های یونیون‌کارت و ویزاکارت': 'Buy UnionCard and VisaCard cards',
    'اخبار ورزشی، اقتصادی، سیاسی و اجتماعی': 'Sports, economic, political, and social news',
    'تازه‌ها و فیچرهای جدید سایت': 'Site updates and new features',
    'پیگیری خریدها و مرحله‌ی سفارش': 'Track purchases and order status',

    # ACDNews / ACDNotes
    'همه': 'All',
    'ورزشی': 'Sports',
    'اقتصادی': 'Economy',
    'سیاسی': 'Politics',
    'اجتماعی': 'Society',
    'هنوز خبری منتشر نشده است. اخبار هر یک از این چهار دسته، همراه با منبع و برچسب‌ها، اینجا نمایش داده می‌شوند.':
        'No news has been published yet. News from each of these four categories, along with its source and tags, will appear here.',
    'هنوز یادداشتی منتشر نشده است. تازه‌ها و فیچرهای جدید سایت اینجا اعلام می‌شوند.':
        'No notes have been published yet. Site updates and new features will be announced here.',
    'بازگشت به ACDNews': 'Back to ACDNews',
    'بازگشت به ACDNotes': 'Back to ACDNotes',
    'منبع': 'Source',
    'خبر فوری': 'Breaking News',

    # My Products
    'هنوز خریدی ثبت نشده است. وقتی کارتی از ACDPay بخرید، همین‌جا لیست می‌شود و می‌توانید مرحله‌ی سفارش را پیگیری کنید:':
        "No purchases yet. Once you buy a card from ACDPay, it'll be listed here and you can track its order status:",
    'بلیط‌های ACDBallons مراحل ساده‌تری دارند (بدون ثبت بانکی و چاپ).':
        'ACDBallons tickets have simpler stages (no bank registration or printing).',

    # Order stages, both flows (apps/shop/models.py: STAGE_LABELS) — the
    # first 6 are shared between ACDPay and ACDBallons; the next 3 are
    # ACDPay-only (card registration/printing/shipping); the last 2 are
    # ACDBallons-only.
    'ثبت درخواست': 'Request submitted',
    'استعلام مدارک': 'Verifying documents',
    'مدارک ارسال شد': 'Documents submitted',
    'راهنمای پرداخت': 'Payment instructions',
    'پرداخت ثبت شد': 'Payment submitted',
    'پرداخت تایید شد': 'Payment confirmed',
    'ثبت کارت در بانک': 'Card registered with bank',
    'در حال چاپ': 'Printing',
    'ارسال شده': 'Shipped',
    'تایید ظرفیت و تاریخ': 'Availability & date confirmed',
    'بلیط صادر شد': 'Ticket issued',

    # Auth pages
    'ورود به حساب کاربری': 'Log in to your account',
    'نام کاربری یا رمز عبور اشتباه است.': 'Incorrect username or password.',
    'حساب کاربری ندارید؟': "Don't have an account?",
    'ثبت‌نام کنید': 'Sign up',
    'ساخت حساب کاربری جدید': 'Create a new account',
    'قبلاً حساب کاربری ساخته‌اید؟': 'Already have an account?',
    'وارد شوید': 'Log in',

    # Profile
    'پروفایل من': 'My profile',
    'نام کاربری': 'Username',
    'ایمیل': 'Email',
    'شماره موبایل': 'Mobile number',
    'ویرایش پروفایل، آواتار و آدرس‌ها در مرحله‌ی بعدی پیاده‌سازی اضافه می‌شود.':
        'Profile editing, avatar, and addresses will be added in the next implementation stage.',

    # ACDSupport
    'پشتیبانی': 'Support',
    'تیکت‌های پشتیبانی': 'Support tickets',
    'تیکت جدید': 'New ticket',
    'ثبت تیکت جدید': 'Submit new ticket',
    'ارسال تیکت': 'Send ticket',
    'ارسال پاسخ': 'Send reply',
    'موضوع': 'Subject',
    'پیام': 'Message',
    'پاسخ شما': 'Your reply',
    'شما': 'You',
    'ثبت تیکت و پیگیری پشتیبانی': 'Submit a ticket and track support',
    'سوال یا مشکلتان را بنویسید؛ پشتیبانی از همین صفحه پاسخ می‌دهد.':
        "Write your question or issue; support will reply right here on this page.",
    'هنوز تیکتی ثبت نکرده‌اید. اگر سوالی دارید یا مشکلی پیش اومده، از همینجا با پشتیبانی در تماس باشید.':
        "You haven't submitted a ticket yet. If you have a question or ran into an issue, get in touch with support here.",
    'بازگشت به تیکت‌ها': 'Back to tickets',
    'این تیکت بسته شده؛ اگر دوباره پیام بدهید، به‌صورت خودکار باز می‌شود.':
        'This ticket is closed; sending another message will automatically reopen it.',
    'تیکت شما ثبت شد؛ پشتیبانی به‌زودی پاسخ می‌دهد.': 'Your ticket has been submitted; support will reply soon.',
    'به‌محض پاسخ پشتیبانی، از طریق زنگوله‌ی بالای سایت به شما اطلاع داده می‌شود.':
        "The moment support replies, you'll be notified via the bell at the top of the site.",
    # Ticket.STATUS_CHOICES (apps/support/models.py) — same plain-string
    # choices pattern as STAGE_LABELS/CATEGORY_CHOICES elsewhere.
    'باز': 'Open',
    'پاسخ داده شده': 'Answered',
    'بسته شده': 'Closed',

    # Floating "chat with admin" widget (apps.support Conversation/
    # ChatMessage — a separate, always-on feature from the ticket system
    # above: no submit-once/admin-only-reply restriction, just a live
    # back-and-forth thread with whoever staffs the admin panel).
    'چت با پشتیبانی': 'Chat with support',
    'هنوز پیامی وجود ندارد. اولین پیام خود را بفرستید.': 'No messages yet. Send the first one.',
    'پیام خود را بنویسید…': 'Write your message…',
    'ارسال': 'Send',
    'ارسال پیام با خطا مواجه شد. دوباره تلاش کنید.': 'Failed to send the message. Please try again.',
    'متن پیام نمی‌تواند خالی باشد.': 'Message text cannot be empty.',

    # Admin panel — app/model names, sidebar nav, and field labels. Django's
    # OWN strings (Personal info, Permissions, Add, Change, "user"/"users",
    # etc.) already come translated from Django's bundled fa catalog; these
    # entries cover everything of OURS the admin couldn't otherwise
    # translate (see translate_lazy below for how these reach
    # verbose_name=, which real gettext_lazy can't do without a compiled
    # catalog — that gap was exactly why the admin looked half-and-half).
    'شاپ': 'Shop',
    'بلاگ': 'Blog',
    'کشور': 'Country',
    'مدیریت سایت': 'Site management',
    'نماینده': 'Representative',
    'نام کشور': 'Country name',
    'پرچم': 'Flag',
    'لینک پرچم': 'Flag URL',
    'تصویر پس‌زمینه': 'Background image',
    'لینک تصویر پس‌زمینه': 'Background image URL',
    'سرود ملی (فایل صوتی)': 'National anthem (audio file)',
    'لینک سرود ملی': 'National anthem URL',
    'توضیحات': 'Description',
    'نام خانوادگی': 'Last name',
    'عکس نماینده': 'Representative photo',
    'لینک عکس نماینده': 'Representative photo URL',
    'عنوان': 'Title',
    'حساب‌های کاربری': 'Accounts',
    'کاربران': 'Users',
    'گروه‌ها': 'Groups',
    'دسته‌بندی': 'Category',
    'دسته‌بندی‌ها': 'Categories',
    'محصول': 'Product',
    'محصولات': 'Products',
    'سفارش': 'Order',
    'سفارش‌ها': 'Orders',
    'پست': 'Post',
    'پست‌ها': 'Posts',
    'نام': 'Name',
    'صفحه': 'Page',
    'ترتیب': 'Sort order',
    'فعال': 'Active',
    'توضیح کوتاه': 'Short description',
    'توضیح کامل': 'Full description',
    'قیمت': 'Price',
    'تصویر': 'Image',
    'لینک تصویر': 'Image URL',
    'تاریخ ایجاد': 'Created at',
    'کاربر': 'User',
    'مرحله': 'Stage',
    'شماره تماس': 'Contact number',
    'یادداشت داخلی': 'Internal note',
    'مخفی از مشتری': 'Hidden from customer',
    'آخرین بروزرسانی': 'Last updated',
    'کانال انتشار': 'Publish channel',
    'بخش خبری': 'News section',
    'نامک': 'Slug',
    'خلاصه': 'Summary',
    'متن کامل': 'Body',
    'تگ‌ها': 'Tags',
    'نام منبع': 'Source name',
    'لینک منبع': 'Source URL',
    'تاریخ انتشار': 'Published at',
    'محتوا': 'Content',
    'رسانه': 'Media',
    'قیمت و نمایش': 'Price & display',
    'نمایش': 'Display',
    'فقط ACDNews': 'ACDNews only',
    'زمان': 'Time',
    'اطلاعات مشتری': 'Customer info',
    'داخلی': 'Internal',

    # Support/chat field labels (apps/support/models.py, apps/core/models.py).
    # 'متن پیام'/'فرستنده'/'تاریخ ارسال'/'پاسخ پشتیبانی' are shared verbatim
    # between TicketMessage and ChatMessage — one entry here covers both.
    'متن پیام': 'Message text',
    'فرستنده': 'Sender',
    'تاریخ ارسال': 'Sent at',
    'پاسخ پشتیبانی': 'Support reply',
    'خوانده‌شده': 'Read',  # also Notification.is_read (apps/core/models.py)
    'گفتگو': 'Conversation',
    'گفتگوها': 'Conversations',
    'آخرین پیام': 'Last message',
    'پیام گفتگو': 'Chat message',
    'پیام‌های گفتگو': 'Chat messages',
    'پیام‌های بی‌پاسخ': 'Unanswered messages',

    # Country page extras: attractions + travel-route calculator
    # (templates/core/country_detail.html, templates/core/attraction_detail.html)
    'جاذبه‌های گردشگری': 'Tourist attractions',
    'جاذبه‌ای برای این کشور ثبت نشده است.': 'No attractions have been added for this country yet.',
    'توضیحاتی برای این جاذبه ثبت نشده است.': 'No description has been added for this attraction yet.',
    'فاصله و مسیر سفر تا اینجا': 'Distance & travel route to here',
    'کشور مبدا و نوع مسیر رو انتخاب کن تا فاصله و زمان تقریبی سفر رو ببینی.':
        'Pick an origin country and a travel mode to see the distance and estimated travel time.',
    'از کشور': 'From country',
    'انتخاب کنید': 'Select',
    'نوع مسیر': 'Travel mode',
    'نمایش نتیجه': 'Show result',
    'برای این ترکیب مبدا/مسیر هنوز اطلاعاتی ثبت نشده است.': 'No data has been added yet for this origin/mode combination.',
    'هنوز مسیری برای این کشور ثبت نشده است.': 'No travel routes have been added for this country yet.',

    # TRAVEL_MODE_CHOICES (apps/core/models.py)
    'هوایی': 'By air',
    'زمینی (جاده)': 'By land (road)',
    'ریلی (قطار)': 'By rail (train)',
    'دریایی': 'By sea',

    # Hotels (apps/core/models.py Hotel, templates/core/country_detail.html)
    'هتل‌های معروف': 'Famous hotels',
    'هتلی برای این کشور ثبت نشده است.': 'No hotels have been added for this country yet.',
    'آدرس': 'Address',
    'تماس با هتل': 'Hotel phone',
    'رزرو / اطلاعات بیشتر': 'Booking / more info',
    'توضیحاتی برای این هتل ثبت نشده است.': 'No description has been added for this hotel yet.',
    'قیمت تقریبی هر شب': 'Approx. price / night',
    'تومان': 'Toman',
    'نقشه‌ی هتل': 'Hotel map',
    'مقایسه‌ی قیمت هتل‌ها (تومان)': 'Hotel price comparison (Toman)',
    'مقایسه‌ی قیمت هتل‌ها (دلار)': 'Hotel price comparison (USD)',
    'بر اساس نرخ روز دلار؛ این نمودار هر روز به‌طور خودکار به‌روزرسانی می‌شود.': "Based on today's USD exchange rate; this chart refreshes automatically every day.",
    'نرخ امروز': "Today's rate",
    'قیمت پایه به دلار آمریکا، مستقل از نرخ ارز.': 'Base price in US dollars, independent of the exchange rate.',

    # Currency chart (templates/core/country_detail.html)
    'ارزش پول این کشور': "This country's currency value",
    '۱ دلار آمریکا برابر است با:': '1 US dollar equals:',
    'و': 'and',
    'این نرخ هر روز به‌طور خودکار به‌روزرسانی می‌شود.': 'This rate updates automatically every day.',
    '۱ دلار آمریکا': '1 US dollar',

    # Quick facts strip ("کشور در یک نگاه")
    'پایتخت': 'Capital',
    'زبان رسمی': 'Official language',
    'واحد پول': 'Currency',
    'کد تلفن': 'Calling code',
    'بهترین فصل سفر': 'Best time to visit',

    # Route calculator: world-origin estimate note (templates/core/country_detail.html)
    'برای کشورهایی که هنوز مسیر واقعی ثبت نشده، فاصله و زمان به‌صورت تخمینی (بر اساس فاصله مستقیم) نمایش داده می‌شود.':
        "For countries without a confirmed real route yet, the distance and time shown are an estimate (based on straight-line distance).",
    'تخمینی': 'Estimated',

    # Seasonal weather (templates/core/country_detail.html)
    'آب‌وهوا در فصل‌های مختلف': 'Weather by season',
    'بهار': 'Spring',
    'تابستان': 'Summer',
    'پاییز': 'Autumn',
    'زمستان': 'Winter',
}


def translate(persian_text):
    """Returns the English text for `persian_text` when the active
    language is English; returns it unchanged otherwise (including when
    no translation has been added yet, so missing entries fail soft)."""
    if get_language() == 'en':
        return TRANSLATIONS.get(persian_text, persian_text)
    return persian_text


# Lazy version of translate(), for the handful of places that need a value
# *before* a request/active-language exists — model field verbose_name=,
# Meta.verbose_name, AppConfig.verbose_name, admin fieldset section titles,
# Unfold's SIDEBAR nav titles. Those are all evaluated once when their
# module is imported, long before any request sets an active language, so
# calling translate() directly there would always see the default language.
# django.utils.functional.lazy defers the actual call until the value is
# coerced to text (e.g. when a template renders it), at which point the
# request's active language is known — the exact same trick gettext_lazy
# uses, just backed by our own dict instead of a compiled .mo catalog.
translate_lazy = lazy(translate, str)
