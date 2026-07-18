"""
USD-based exchange rates used by:
  - templates/core/country_detail.html — "ارزش پول این کشور" chart (1 USD
    in that country's own currency, and in Toman).

Real-time exchange-rate data isn't something this project has its own feed
for, and standing up a paid FX subscription is out of scope. Instead this
calls a free, no-API-key exchange-rate endpoint once, caches the FULL rates
table for 24 hours via Django's cache framework, and falls back to a
hardcoded approximate table if the request fails (offline dev environment,
endpoint down, etc.) so nothing ever crashes — it just falls back to a
labeled estimate. Because the cache entry expires after a day, the very
next request after that automatically re-fetches, which is what gives us
"updates every day" without needing a cron job or Celery beat schedule.

Uses only the Python standard library (urllib) on purpose — no `requests`
dependency to install, since one flaky pip mirror shouldn't be able to
block this feature from working at all.
"""
import json
import logging
import urllib.request

from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_KEY = 'acd_usd_rates_table'
CACHE_TIMEOUT_SECONDS = 60 * 60 * 24  # 24h — see module docstring.

# Free, keyless endpoint: https://www.exchangerate-api.com/docs/free (open.er-api.com mirror)
USD_RATES_API_URL = 'https://open.er-api.com/v6/latest/USD'

# Used only if the live fetch fails. Units of each currency per 1 USD, plus
# IRR (Rial — Toman is IRR / 10). Rough, manually-maintained backstop —
# real traffic will almost always hit the live-fetched, cached table
# instead. Covers every currency code used by apps/core/currency_codes.py.
FALLBACK_RATES = {
    'IRR': 600000, 'AFN': 70, 'BHD': 0.376, 'BDT': 120, 'BTN': 84,
    'BND': 1.34, 'KHR': 4100, 'CNY': 7.2, 'INR': 84, 'IDR': 16200,
    'JPY': 152, 'JOD': 0.709, 'KZT': 480, 'KWD': 0.307, 'KGS': 87,
    'LAK': 21700, 'MYR': 4.4, 'MNT': 3450, 'MMK': 2100, 'NPR': 134,
    'OMR': 0.385, 'PKR': 278, 'PHP': 58, 'QAR': 3.64, 'RUB': 92,
    'SAR': 3.75, 'SGD': 1.34, 'KRW': 1380, 'LKR': 300, 'TJS': 10.9,
    'THB': 34.5, 'TRY': 34, 'AED': 3.6725, 'UZS': 12700, 'VND': 25400,
    'AMD': 388, 'AZN': 1.7, 'EUR': 0.92, 'GEL': 2.7, 'IQD': 1310,
    'ILS': 3.7, 'LBP': 89500, 'MVR': 15.4, 'KPW': 900, 'SYP': 13000,
    'TWD': 32, 'TMT': 3.5, 'YER': 250, 'USD': 1,
}


def _fetch_live_rates():
    """Returns the full {code: units_per_usd} dict or None on any failure."""
    try:
        request = urllib.request.Request(USD_RATES_API_URL, headers={'User-Agent': 'ACDZone/1.0'})
        with urllib.request.urlopen(request, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
        rates = data.get('rates')
        return rates or None
    except Exception:
        logger.warning('Live exchange-rate fetch failed; using fallback table.', exc_info=True)
        return None


def get_usd_rates():
    """The full {currency_code: units_per_1_USD} table, cached for a day
    at a time — see module docstring for why that alone is enough to
    satisfy "update every day" without extra infrastructure."""
    rates = cache.get(CACHE_KEY)
    if rates is not None:
        return rates
    rates = _fetch_live_rates() or FALLBACK_RATES
    cache.set(CACHE_KEY, rates, CACHE_TIMEOUT_SECONDS)
    return rates


def get_usd_to_toman_rate():
    """Toman per 1 USD (Rial / 10)."""
    rates = get_usd_rates()
    rial = rates.get('IRR') or FALLBACK_RATES['IRR']
    return float(rial) / 10
