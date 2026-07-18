import json
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timesince import timesince
from django.utils.translation import get_language
from django.views.decorators.http import require_GET, require_POST

from urllib.parse import quote

from apps.blog.models import Post
from apps.core.currency_codes import CURRENCY_CODES
from apps.core.exchange_rate import get_usd_rates, get_usd_to_toman_rate
from apps.core.geo import estimate_flight_duration_text, haversine_km
from apps.core.models import Attraction, Country, Hotel, Notification, Representative, TravelRoute, TRAVEL_MODE_CHOICES, TRAVEL_MODE_ICONS
from apps.core.translations import translate
from apps.core.world_countries import OWN_COUNTRY_COORDS, WORLD_COUNTRIES
from apps.shop.models import Product

# Drop the intro video here (exact filename matters) and the home page will
# start showing it automatically — no code change needed. Same for the
# Persian subtitle track. See README for how these get generated.
INTRO_VIDEO_REL_PATH = 'video/intro.mp4'
INTRO_SUBTITLE_REL_PATH = 'video/intro-fa.vtt'


def home(request):
    context = {
        # Real Category/Product models now exist (apps/shop/models.py) —
        # add/edit/reorder products from the admin panel and they show up
        # here automatically, no code change needed. Empty until the admin
        # adds the first product.
        'products_preview': (
            Product.objects.filter(is_active=True, category__is_active=True)
            .select_related('category')[:4]
        ),
        # Real Post model now exists (apps/blog/models.py) — mixes both
        # channels together, most recent first, same idea as products_preview.
        # '-is_urgent' first: urgent posts always float to the top regardless
        # of published_at, matching ACDNews/ACDNotes' own ordering.
        'latest_posts': Post.objects.filter(is_active=True).order_by('-is_urgent', '-published_at')[:3],
        'intro_video_exists': os.path.exists(
            os.path.join(settings.BASE_DIR, 'static', INTRO_VIDEO_REL_PATH)
        ),
        'intro_subtitle_exists': os.path.exists(
            os.path.join(settings.BASE_DIR, 'static', INTRO_SUBTITLE_REL_PATH)
        ),
    }
    return render(request, 'core/home.html', context)


def dashboard(request):
    # Open to signed-out visitors on purpose — it's just a menu of links
    # to other pages (most of them public), so gating the menu itself
    # made the whole site feel closed off. The tiles that point at
    # actually personal data (my_products, support:ticket_list) still
    # carry their own @login_required and will redirect to login if a
    # guest clicks through to them; only the "خرید" action gets the nicer
    # auth-required modal instead of a hard redirect (see
    # templates/partials/auth_required_modal.html).
    return render(request, 'core/dashboard.html')


def country_detail(request, slug):
    """Landing page for one entry in the header's "کشورها" dropdown.
    is_active=True is enforced here too (not just in the dropdown query in
    apps/core/context_processors.py) so a deactivated country's page 404s
    even if someone already has the old link saved/shared."""
    country = get_object_or_404(Country, slug=slug, is_active=True)

    attractions = country.attractions.filter(is_active=True)
    hotels = country.hotels.filter(is_active=True)

    # Route-calculator data (templates/core/country_detail.html): the user
    # asked for the origin dropdown to list literally every country in the
    # world, not just the handful this site happens to have curated real
    # TravelRoute rows for. Two layers, both keyed by the same string
    # "origin_id" (a Country.slug for one of this site's own 50 countries,
    # or a plain code from apps/core/world_countries.py for everywhere
    # else) so static/js/main.js's existing matching logic needs no changes:
    #
    #   1. Curated rows (admin-entered, real data, any of the four modes)
    #      — always shown first/preferred when they exist for a given
    #      origin+mode.
    #   2. A computed "estimated flight" entry (mode='air') for every
    #      OTHER country on Earth, using great-circle distance from
    #      apps/core/geo.py — clearly labeled as an estimate. Skipped for
    #      any origin that already has a curated 'air' row, so the real
    #      data always wins over the guess.
    curated_routes = (
        TravelRoute.objects
        .filter(destination_country=country, is_active=True)
        .select_related('origin_country')
    )
    routes_data = [
        {
            'origin_id': route.origin_country.slug,
            'mode': route.mode,
            'mode_label': route.get_mode_display(),
            'icon': TRAVEL_MODE_ICONS.get(route.mode, 'signpost-2'),
            'distance_km': route.distance_km,
            'duration_text': route.duration_text,
            'notes': route.notes,
            'is_estimate': False,
        }
        for route in curated_routes
    ]
    curated_air_origins = {
        route.origin_country.slug for route in curated_routes if route.mode == 'air'
    }

    dest_coords = OWN_COUNTRY_COORDS.get(country.slug)
    lang = get_language() or 'fa'
    is_fa = lang.startswith('fa')
    estimate_note_fa = 'فاصله و زمان تقریبی بر اساس خط مستقیم؛ پرواز واقعی معمولاً طولانی‌تر است.'
    estimate_note_en = 'Approximate straight-line distance/time; real flights usually take longer.'

    world_origins = []  # for the dropdown: every country except this one
    if dest_coords:
        dest_lat, dest_lon = dest_coords

        # Our own 50 countries first (they also get a link-worthy slug).
        for other in Country.objects.filter(is_active=True).exclude(pk=country.pk):
            coords = OWN_COUNTRY_COORDS.get(other.slug)
            world_origins.append({'code': other.slug, 'name': other.name})
            if coords and other.slug not in curated_air_origins:
                distance_km = haversine_km(dest_lat, dest_lon, coords[0], coords[1])
                routes_data.append({
                    'origin_id': other.slug,
                    'mode': 'air',
                    'mode_label': translate('هوایی'),
                    'icon': TRAVEL_MODE_ICONS.get('air', 'airplane'),
                    'distance_km': distance_km,
                    'duration_text': estimate_flight_duration_text(distance_km, 'fa' if is_fa else 'en'),
                    'notes': estimate_note_fa if is_fa else estimate_note_en,
                    'is_estimate': True,
                })

        # Every other country on Earth (apps/core/world_countries.py).
        for code, (name_fa, name_en, lat, lon) in WORLD_COUNTRIES.items():
            world_origins.append({'code': code, 'name': name_fa if is_fa else name_en})
            if code in curated_air_origins:
                continue
            distance_km = haversine_km(dest_lat, dest_lon, lat, lon)
            routes_data.append({
                'origin_id': code,
                'mode': 'air',
                'mode_label': translate('هوایی'),
                'icon': TRAVEL_MODE_ICONS.get('air', 'airplane'),
                'distance_km': distance_km,
                'duration_text': estimate_flight_duration_text(distance_km, 'fa' if is_fa else 'en'),
                'notes': estimate_note_fa if is_fa else estimate_note_en,
                'is_estimate': True,
            })

    world_origins.sort(key=lambda o: o['name'])

    # Currency chart data: 1 USD expressed in this country's own currency
    # and in Toman — see apps/core/exchange_rate.py for the daily-cached
    # live fetch + fallback table this is built from. Rendered as plain
    # CSS bars in the template (see bar width % computed below), not a JS
    # charting library — a prior version used Chart.js loaded from
    # cdnjs.cloudflare.com, which showed up blank for this site's
    # Iran-based audience because that CDN is commonly blocked/filtered
    # there. Pure CSS bars can't fail that way: no script to fetch, no
    # network dependency, nothing to silently not-load.
    currency_code = CURRENCY_CODES.get(country.slug)
    rates = get_usd_rates()
    toman_rate = get_usd_to_toman_rate()
    local_units_per_usd = rates.get(currency_code) if currency_code else None
    has_currency_chart = bool(local_units_per_usd) and currency_code != 'IRR'

    local_bar_pct = toman_bar_pct = None
    if has_currency_chart:
        max_val = max(float(local_units_per_usd), float(toman_rate))
        local_bar_pct = max(4, round(float(local_units_per_usd) / max_val * 100, 1))
        toman_bar_pct = max(4, round(float(toman_rate) / max_val * 100, 1))

    context = {
        'country': country,
        'attractions': attractions,
        'hotels': hotels,
        'world_origins': world_origins,
        'travel_modes': TRAVEL_MODE_CHOICES,
        'routes_json': json.dumps(routes_data),
        'has_routes': bool(routes_data),
        'has_currency_chart': has_currency_chart,
        'local_units_per_usd': local_units_per_usd,
        'toman_rate': toman_rate,
        'currency_code': currency_code,
        'local_bar_pct': local_bar_pct,
        'toman_bar_pct': toman_bar_pct,
    }
    return render(request, 'core/country_detail.html', context)


def attraction_detail(request, country_slug, attraction_slug):
    """Full page for one attraction card from a country's "جاذبه‌های
    گردشگری" section — photo + complete description."""
    attraction = get_object_or_404(
        Attraction.objects.select_related('country'),
        slug=attraction_slug,
        country__slug=country_slug,
        is_active=True,
        country__is_active=True,
    )
    return render(request, 'core/attraction_detail.html', {'attraction': attraction})


def hotel_detail(request, country_slug, hotel_slug):
    """Full page for one hotel card from a country's "هتل‌های معروف"
    section — photo, star rating, address, phone number, an embedded map,
    and (when price_usd is set) its approximate nightly price in USD and
    Toman using the day's cached exchange rate (see
    apps/core/exchange_rate.py — that cache is what makes the Toman
    conversion "update every day" without any extra cron/Celery
    infrastructure). The bar-chart version of this was removed after it
    rendered blank for some visitors; the price is shown as plain text
    instead. The currency-value chart lives on the country page instead
    (see country_detail() above)."""
    hotel = get_object_or_404(
        Hotel.objects.select_related('country'),
        slug=hotel_slug,
        country__slug=country_slug,
        is_active=True,
        country__is_active=True,
    )

    toman_rate = get_usd_to_toman_rate()
    price_toman = None
    if hotel.price_usd is not None:
        price_toman = round(float(hotel.price_usd) * toman_rate)

    maps_query = quote(f'{hotel.name} {hotel.address or hotel.city or hotel.country.name}')
    maps_embed_url = f'https://www.google.com/maps?q={maps_query}&output=embed'

    context = {
        'hotel': hotel,
        'price_toman': price_toman,
        'maps_embed_url': maps_embed_url,
    }
    return render(request, 'core/hotel_detail.html', context)


def representative_detail(request, slug):
    """Public profile page for one representative in the header dropdown."""
    representative = get_object_or_404(
        Representative.objects.select_related('country'),
        slug=slug,
        is_active=True,
        country__is_active=True,
    )
    return render(request, 'core/representative_detail.html', {'representative': representative})


@login_required
def notification_open(request, pk):
    """Bell-dropdown item click: mark that one notification read, then send
    the user on to whatever it's actually about (an order, a post, ...).
    Scoped to request.user so nobody can mark/open another user's
    notification just by guessing a pk."""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=['is_read'])
    return redirect(notification.link or 'core:home')


@login_required
@require_POST
def notifications_mark_all_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'ok': True})


# --- Bell dropdown (AJAX) ----------------------------------------------
#
# Same reasoning as apps/support/views.py's chat_unread_count/chat_messages:
# the count on the closed bell needs to update on its own while someone
# sits on a page without navigating (e.g. a staff reply arrives while
# they're reading the home page) — the context processor alone
# (apps/core/context_processors.py) only recomputes on a fresh page
# render, so it can't do that by itself. These two endpoints let
# static/js/notifications.js poll the count quietly, and refetch the
# full list the moment the dropdown is actually opened.

@login_required
@require_GET
def notifications_unread_count(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})


@login_required
@require_GET
def notifications_list(request):
    payload = [
        {
            'id': note.pk,
            'message': note.message,
            'time_label': f'{timesince(note.created_at)} {translate("پیش")}',
            'is_read': note.is_read,
            # Routes through notification_open (not note.link directly) so
            # clicking it from this AJAX-rendered list still marks that
            # one notification read before redirecting, exactly like the
            # plain server-rendered {% url %} link it replaces.
            'open_url': reverse('core:notification_open', args=[note.pk]),
        }
        for note in request.user.notifications.all()[:8]
    ]
    return JsonResponse({
        'notifications': payload,
        # Piggybacks the fresh count on the same response so the widget
        # doesn't need a second request while the dropdown is open — one
        # fetch refreshes both the list and the badge at once.
        'unread_count': request.user.notifications.filter(is_read=False).count(),
    })
