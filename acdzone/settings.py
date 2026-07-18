"""
Django settings for the acdzone project.

Architecture decisions locked in for this project (see project README for
the reasoning behind each):
  - Server-rendered Django templates + Bootstrap 5 (RTL build for Persian).
  - django-modeltranslation for bilingual (fa/en) database content.
  - SQLite for local development, swappable to PostgreSQL later via
    the DATABASE_URL environment variable (no code changes needed).
  - django-unfold for a modern, bilingual-friendly admin theme.
"""

from pathlib import Path

import environ
from django.contrib.messages import constants as message_constants
from django.templatetags.static import static
from django.urls import reverse_lazy

from apps.core.translations import translate_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
# Read the .env file if present. Copy .env.example to .env and fill it in.
environ.Env.read_env(BASE_DIR / '.env')


# ------------------------------------------------------------------------
# Core / security
# ------------------------------------------------------------------------

SECRET_KEY = env(
    'SECRET_KEY',
    default='django-insecure-CHANGE-ME-this-is-only-for-first-run-do-not-deploy',
)

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])


# ------------------------------------------------------------------------
# Applications
# ------------------------------------------------------------------------

INSTALLED_APPS = [
    # Admin theme must be listed before django.contrib.admin (unfold requirement)
    'unfold',

    # modeltranslation must ALSO be listed before django.contrib.admin: its
    # app ready() hook is what registers Category/Product for translation
    # (apps/shop/translation.py), and that registration has to exist before
    # admin autodiscovery imports apps/shop/admin.py — which builds
    # TranslationAdmin classes for those same models. If admin comes first,
    # autodiscovery crashes with "NotRegistered: The model ... is not
    # registered for translation" (this bit us once — see README).
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Local apps
    'apps.accounts',
    'apps.core',
    'apps.shop',
    'apps.blog',
    'apps.support',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # must come after Session, before Common
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'acdzone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'acdzone.wsgi.application'
ASGI_APPLICATION = 'acdzone.asgi.application'


# ------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------
# Defaults to SQLite (chosen for the initial build/test phase), built as a
# plain dict rather than parsed from a URL so a Windows filesystem path
# never has to survive a round-trip through URL parsing.
#
# To move to PostgreSQL later: install psycopg2-binary and set
# ACDZONE_DATABASE_URL in .env to something like
# postgres://USER:PASSWORD@HOST:5432/DBNAME — as soon as that variable is
# set, it takes over automatically. No code changes required either way.
#
# Deliberately NOT named plain "DATABASE_URL": that name is a very common
# convention (Prisma, Rails, Heroku, etc.) and if any other tool/project on
# this machine has already set a system-wide DATABASE_URL environment
# variable, Django would silently pick that up instead of this project's
# .env value — which is exactly what happened the first time (a stray
# DATABASE_URL pointing at MongoDB was already set on this machine). Using
# a project-namespaced name avoids that collision entirely.

if env('ACDZONE_DATABASE_URL', default=None):
    DATABASES = {'default': env.db('ACDZONE_DATABASE_URL')}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ------------------------------------------------------------------------
# Telegram support-chat bridge (apps/support/telegram_bot.py)
# ------------------------------------------------------------------------
# Both optional — apps/support/telegram_bot.py silently no-ops if either
# is blank, so the on-site chat widget works with zero Telegram setup.
# See the README's Telegram section for how to get a real bot token (via
# @BotFather) and the support group's chat_id.
TELEGRAM_BOT_TOKEN = env('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_SUPPORT_CHAT_ID = env('TELEGRAM_SUPPORT_CHAT_ID', default='')


# ------------------------------------------------------------------------
# Auth
# ------------------------------------------------------------------------

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

# Bootstrap uses "danger", not "error", for its red alert class.
MESSAGE_TAGS = {
    message_constants.ERROR: 'danger',
}


# ------------------------------------------------------------------------
# Internationalization (site is bilingual: Persian + English)
# ------------------------------------------------------------------------

LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('fa', 'فارسی'),
    ('en', 'English'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

# django-modeltranslation: languages available for database content
# (product names, post bodies, etc.) once models register TranslationOptions
# in a per-app translation.py — see README "next steps".
MODELTRANSLATION_DEFAULT_LANGUAGE = 'fa'
MODELTRANSLATION_LANGUAGES = ('fa', 'en')
MODELTRANSLATION_FALLBACK_LANGUAGES = ('fa', 'en')


# ------------------------------------------------------------------------
# Static & media files
# ------------------------------------------------------------------------

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ------------------------------------------------------------------------
# django-unfold (admin theme) — bilingual, customizable admin panel
# See https://unfoldadmin.com/docs/ for the full configuration reference.
# Config keys below were checked against the actually-installed version's
# source (venv/Lib/site-packages/unfold) rather than assumed from memory —
# in particular unfold/utils.py's convert_color() (confirms the COLORS
# format used here) and unfold/templates/unfold/helpers/app_list.html
# (confirms the SIDEBAR "collapsible" behaviour).
# ------------------------------------------------------------------------

UNFOLD = {
    'SITE_TITLE': 'ACD Zone Admin',
    'SITE_HEADER': 'ACD Zone',
    'SHOW_LANGUAGES': True,
    # NOTE: deliberately NOT forcing 'dark' here (that was tried and
    # reverted). Forcing dark mode meant Unfold's light-on-dark text
    # classes took over everywhere — the opposite of "black text
    # visible" — and black text is never readable against a dark
    # surface, forced or not. Leaving THEME unset restores Unfold's
    # normal light/dark toggle (defaults to the browser's preference),
    # so body text is dark-on-light by default like the request asks.
    # The logo's legibility concern that originally motivated forcing
    # dark mode is solved differently now: the sidebar itself has an
    # explicit green background (see static/css/admin-custom.css,
    # #nav-sidebar-inner) matching the public site's header, so the
    # cream/gold logo reads fine against it regardless of light/dark mode.
    'SITE_ICON': lambda request: static('img/favicon.svg'),
    'SITE_LOGO': lambda request: static('img/logo.svg'),
    'SITE_FAVICONS': [
        {
            'rel': 'icon',
            'sizes': '32x32',
            'type': 'image/svg+xml',
            'href': lambda request: static('img/favicon.svg'),
        },
    ],
    # Extra CSS loaded on every admin page: RTL text-alignment fixes for
    # the handful of Unfold templates that hardcode Tailwind's `text-left`
    # utility, plus the green-primary/red-on-hover interaction colors. See
    # static/css/admin-custom.css for the full reasoning.
    'STYLES': [
        lambda request: static('css/admin-custom.css'),
    ],
    # Same deep-emerald brand color as the public site (static/css/style.css
    # --acd-emerald: #0b4f3c), expressed as an 11-step shade ramp anchored
    # at 600 — unchanged, already correct (convert_color() accepts this
    # space-separated "R G B" form and turns it into rgb(R, G, B)). 'base'
    # is new: Unfold's default is a cold blue-gray neutral, which is why
    # the admin looked visibly different from the site's warm cream/ink
    # neutrals even with the emerald primary already in place — this ramp
    # is anchored on --acd-cream (#f8f3e9, ~50) and --acd-ink (#2a2520,
    # ~900) so every neutral surface (backgrounds, borders, body text)
    # reads as the same "warm quiet-luxury" palette as the public site.
    'COLORS': {
        'primary': {
            '50': '232 248 240',
            '100': '205 238 224',
            '200': '158 217 196',
            '300': '105 190 165',
            '400': '56 158 130',
            '500': '21 110 87',
            '600': '11 79 60',
            '700': '8 61 46',
            '800': '6 46 35',
            '900': '4 33 25',
            '950': '2 20 15',
        },
        'base': {
            '50': '#faf7f0',
            '100': '#f3ecdd',
            '200': '#e8dcc3',
            '300': '#d9c7a3',
            '400': '#b8a17d',
            '500': '#8f7a5c',
            '600': '#6b5a44',
            '700': '#4f4433',
            '800': '#382f24',
            '900': '#241f18',
            '950': '#15120d',
        },
    },
    'EXTENSIONS': {
        'modeltranslation': {
            'flags': {
                'fa': '🇮🇷',
                'en': '🇬🇧',
            },
        },
    },
    # Custom sidebar so each app's models sit in their own collapsible
    # group — closed by default, opens on click (or automatically, if the
    # page you're on belongs to that group). Without this, Unfold's
    # default sidebar lists every app's models in a permanently-expanded
    # plain list.
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': _('مدیریت سایت'),
                'separator': False,
                'collapsible': True,
                'items': [
                    {
                        'title': _('داشبورد'),
                        'icon': 'dashboard',
                        'link': reverse_lazy('admin:index'),
                    },
                    {
                        'title': _('اعلان‌ها'),
                        'icon': 'notifications',
                        'link': reverse_lazy('admin:core_notification_changelist'),
                    },
                    {
                        'title': _('کشورها'),
                        'icon': 'public',
                        'link': reverse_lazy('admin:core_country_changelist'),
                    },
                    {
                        'title': _('نماینده‌ها'),
                        'icon': 'badge',
                        'link': reverse_lazy('admin:core_representative_changelist'),
                    },
                    {
                        'title': _('جاذبه‌های گردشگری'),
                        'icon': 'attractions',
                        'link': reverse_lazy('admin:core_attraction_changelist'),
                    },
                    {
                        'title': _('مسیرهای سفر'),
                        'icon': 'route',
                        'link': reverse_lazy('admin:core_travelroute_changelist'),
                    },
                    {
                        'title': _('هتل‌های معروف'),
                        'icon': 'hotel',
                        'link': reverse_lazy('admin:core_hotel_changelist'),
                    },
                ],
            },
            {
                'title': _('حساب‌های کاربری'),
                'separator': True,
                'collapsible': True,
                'items': [
                    {
                        'title': _('کاربران'),
                        'icon': 'group',
                        'link': reverse_lazy('admin:accounts_user_changelist'),
                    },
                    {
                        'title': _('گروه‌ها'),
                        'icon': 'shield_person',
                        'link': reverse_lazy('admin:auth_group_changelist'),
                    },
                ],
            },
            {
                'title': _('شاپ'),
                'separator': True,
                'collapsible': True,
                'items': [
                    {
                        'title': _('دسته‌بندی‌ها'),
                        'icon': 'category',
                        'link': reverse_lazy('admin:shop_category_changelist'),
                    },
                    {
                        'title': _('محصولات'),
                        'icon': 'inventory_2',
                        'link': reverse_lazy('admin:shop_product_changelist'),
                    },
                    {
                        'title': _('سفارش‌ها'),
                        'icon': 'receipt_long',
                        'link': reverse_lazy('admin:shop_order_changelist'),
                    },
                ],
            },
            {
                'title': _('بلاگ'),
                'separator': True,
                'collapsible': True,
                'items': [
                    {
                        'title': _('پست‌ها'),
                        'icon': 'article',
                        'link': reverse_lazy('admin:blog_post_changelist'),
                    },
                ],
            },
            {
                'title': _('پشتیبانی'),
                'separator': True,
                'collapsible': True,
                'items': [
                    {
                        'title': _('تیکت‌ها'),
                        'icon': 'confirmation_number',
                        'link': reverse_lazy('admin:support_ticket_changelist'),
                    },
                    {
                        'title': _('گفتگوها'),
                        'icon': 'chat',
                        'link': reverse_lazy('admin:support_conversation_changelist'),
                        # Unlike icon/link above (which accept a plain
                        # lambda), Unfold's badge resolver specifically
                        # import_strings this as a dotted path and calls
                        # it with request (see unfold/sites.py
                        # _get_navigation_items) — has to be a string.
                        'badge': 'apps.support.badges.unanswered_chat_count',
                    },
                ],
            },
        ],
    },
}
