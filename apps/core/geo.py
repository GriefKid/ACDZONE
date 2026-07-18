"""
Straight-line (great-circle) distance + a rough flight-time estimate,
used by country_detail() in apps/core/views.py to power the route
calculator's "world origin" mode — see apps/core/world_countries.py for
the lat/lon this is computed from.

This is deliberately simple and clearly labeled as an ESTIMATE in the UI
(templates/core/country_detail.html) wherever it's shown: real flights
don't fly a straight line (layovers, airspace, routing), so this will
usually undershoot the real distance a bit. It exists so the route
calculator can offer literally every country in the world as an origin
without needing a real curated TravelRoute row for each of the ~9,700
possible pairs — see apps/core/models.py's TravelRoute docstring for why
that curated data is still kept and preferred when it exists.
"""
import math

EARTH_RADIUS_KM = 6371
# Rough average, blending cruise speed with taxi/climb/descent/boarding
# overhead — good enough for a "roughly how long" estimate, not a
# real-airline timetable.
AVG_EFFECTIVE_SPEED_KMH = 700
FIXED_OVERHEAD_HOURS = 1.0


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return round(EARTH_RADIUS_KM * 2 * math.asin(math.sqrt(a)))


def estimate_flight_duration_text(distance_km, lang='fa'):
    hours = distance_km / AVG_EFFECTIVE_SPEED_KMH + FIXED_OVERHEAD_HOURS
    total_minutes = round(hours * 60)
    h, m = divmod(total_minutes, 60)
    if lang == 'fa':
        parts = []
        if h:
            parts.append(f'{h} ساعت')
        if m:
            parts.append(f'{m} دقیقه')
        return 'حدود ' + ' و '.join(parts) + ' پرواز (تخمینی)' if parts else 'کمتر از یک ساعت پرواز (تخمینی)'
    parts = []
    if h:
        parts.append(f'{h}h')
    if m:
        parts.append(f'{m}m')
    return 'About ' + ' '.join(parts) + ' flight (estimated)' if parts else 'Under 1 hour flight (estimated)'
