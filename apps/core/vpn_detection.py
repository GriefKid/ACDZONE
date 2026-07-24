"""Best-effort VPN, proxy, and Tor detection for public site requests."""

from __future__ import annotations

import hashlib
import ipaddress
import json
import logging
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.cache import cache


logger = logging.getLogger(__name__)


def _parse_ip(value):
    """Return a normalized IP address object, or None for invalid input."""
    if not value:
        return None
    try:
        return ipaddress.ip_address(value.strip())
    except ValueError:
        return None


def _client_ip(request):
    """
    Resolve the public client IP without blindly trusting X-Forwarded-For.

    A forwarding header is accepted only when REMOTE_ADDR is private or
    loopback, which is the normal cPanel/reverse-proxy arrangement. When the
    request reaches Django directly from a public address, a visitor cannot
    spoof the address by supplying their own X-Forwarded-For header.
    """
    remote_ip = _parse_ip(request.META.get('REMOTE_ADDR'))
    if remote_ip is None:
        return None

    if not remote_ip.is_global:
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
        forwarded_ip = _parse_ip(forwarded_for.split(',', 1)[0])
        if forwarded_ip is not None and forwarded_ip.is_global:
            return str(forwarded_ip)

    return str(remote_ip)


def _clear_status(*, checked=False):
    return {
        'blocked': False,
        'checked': checked,
        'reason': '',
    }


def get_vpn_status(request):
    """
    Return the connection status used by the site-wide blocking modal.

    Provider failures intentionally fail open: a quota, DNS, or network
    problem must never make the whole website unavailable.
    """
    if not getattr(settings, 'VPN_DETECTION_ENABLED', True):
        return _clear_status()

    client_ip = _client_ip(request)
    parsed_ip = _parse_ip(client_ip)
    if parsed_ip is None or not parsed_ip.is_global:
        return _clear_status()

    cache_suffix = hashlib.sha256(client_ip.encode('utf-8')).hexdigest()
    cache_key = f'acdzone:vpn-status:{cache_suffix}'
    cached_status = cache.get(cache_key)
    if cached_status is not None:
        return cached_status

    api_url = getattr(
        settings,
        'VPN_DETECTION_API_URL',
        'https://api.ipquery.io/{ip}',
    )
    if '{ip}' in api_url:
        request_url = api_url.format(
            ip=urllib.parse.quote(client_ip, safe=''),
        )
    else:
        separator = '&' if '?' in api_url else '?'
        request_url = f'{api_url}{separator}{urllib.parse.urlencode({"q": client_ip})}'
    provider_request = urllib.request.Request(
        request_url,
        headers={
            'Accept': 'application/json',
            'User-Agent': 'ACDZone/1.0 VPN detection',
        },
    )

    try:
        with urllib.request.urlopen(
            provider_request,
            timeout=getattr(settings, 'VPN_DETECTION_TIMEOUT_SECONDS', 3),
        ) as response:
            if getattr(response, 'status', 200) != 200:
                raise OSError(f'VPN provider returned HTTP {response.status}')
            payload = json.loads(response.read().decode('utf-8'))
    except (OSError, ValueError) as error:
        logger.warning('VPN detection failed open for request: %s', error)
        status = _clear_status()
        cache.set(
            cache_key,
            status,
            getattr(settings, 'VPN_DETECTION_FAILURE_CACHE_SECONDS', 300),
        )
        return status

    risk = payload.get('risk', payload)
    reason = ''
    if risk.get('is_vpn') is True:
        reason = 'vpn'
    elif risk.get('is_proxy') is True:
        reason = 'proxy'
    elif risk.get('is_tor') is True:
        reason = 'tor'
    elif (
        risk.get('is_datacenter') is True
        and getattr(settings, 'VPN_DETECTION_BLOCK_DATACENTER', True)
    ):
        reason = 'datacenter'

    status = {
        'blocked': bool(reason),
        'checked': True,
        'reason': reason,
    }
    cache.set(
        cache_key,
        status,
        getattr(settings, 'VPN_DETECTION_CACHE_SECONDS', 43200),
    )
    return status
