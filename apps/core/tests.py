import json
from unittest.mock import patch

from django.core.cache import cache
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings

from apps.core.vpn_detection import _client_ip, get_vpn_status


class FakeProviderResponse:
    status = 200

    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return json.dumps(self.payload).encode('utf-8')


@override_settings(
    VPN_DETECTION_ENABLED=True,
    VPN_DETECTION_BLOCK_DATACENTER=True,
    VPN_DETECTION_API_URL='https://api.ipquery.io/{ip}',
    VPN_DETECTION_TIMEOUT_SECONDS=1,
    VPN_DETECTION_CACHE_SECONDS=43200,
    VPN_DETECTION_FAILURE_CACHE_SECONDS=300,
)
class VpnDetectionTests(SimpleTestCase):
    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()

    def request_for(self, ip='8.8.8.8', **headers):
        return self.factory.get('/', REMOTE_ADDR=ip, **headers)

    @patch('apps.core.vpn_detection.urllib.request.urlopen')
    def test_private_ip_skips_external_provider(self, urlopen):
        status = get_vpn_status(self.request_for('127.0.0.1'))

        self.assertFalse(status['blocked'])
        self.assertFalse(status['checked'])
        urlopen.assert_not_called()

    @patch('apps.core.vpn_detection.urllib.request.urlopen')
    def test_vpn_response_blocks_and_is_cached(self, urlopen):
        urlopen.return_value = FakeProviderResponse({
            'risk': {
                'is_vpn': True,
                'is_proxy': False,
                'is_tor': False,
                'is_datacenter': True,
            },
        })

        first_status = get_vpn_status(self.request_for())
        second_status = get_vpn_status(self.request_for())

        self.assertEqual(first_status, {
            'blocked': True,
            'checked': True,
            'reason': 'vpn',
        })
        self.assertEqual(second_status, first_status)
        urlopen.assert_called_once()

    @patch('apps.core.vpn_detection.urllib.request.urlopen')
    def test_clean_response_allows_request(self, urlopen):
        urlopen.return_value = FakeProviderResponse({
            'risk': {
                'is_vpn': False,
                'is_proxy': False,
                'is_tor': False,
                'is_datacenter': False,
            },
        })

        status = get_vpn_status(self.request_for())

        self.assertFalse(status['blocked'])
        self.assertTrue(status['checked'])

    @patch('apps.core.vpn_detection.urllib.request.urlopen')
    def test_datacenter_response_blocks_commercial_vpn_exit(self, urlopen):
        urlopen.return_value = FakeProviderResponse({
            'risk': {
                'is_vpn': False,
                'is_proxy': False,
                'is_tor': False,
                'is_datacenter': True,
            },
        })

        status = get_vpn_status(self.request_for())

        self.assertTrue(status['blocked'])
        self.assertEqual(status['reason'], 'datacenter')

    @patch(
        'apps.core.vpn_detection.urllib.request.urlopen',
        side_effect=OSError('provider unavailable'),
    )
    def test_provider_failure_fails_open(self, urlopen):
        status = get_vpn_status(self.request_for())

        self.assertFalse(status['blocked'])
        self.assertFalse(status['checked'])
        urlopen.assert_called_once()

    def test_forwarded_ip_is_trusted_only_behind_private_proxy(self):
        private_proxy_request = self.request_for(
            '10.0.0.5',
            HTTP_X_FORWARDED_FOR='1.1.1.1, 10.0.0.4',
        )
        public_direct_request = self.request_for(
            '8.8.8.8',
            HTTP_X_FORWARDED_FOR='1.1.1.1',
        )

        self.assertEqual(_client_ip(private_proxy_request), '1.1.1.1')
        self.assertEqual(_client_ip(public_direct_request), '8.8.8.8')

    def test_blocking_modal_renders_persian_copy(self):
        html = render_to_string('partials/vpn_block_modal.html', {
            'LANGUAGE_CODE': 'fa',
            'vpn_status': {'blocked': True, 'checked': True, 'reason': 'proxy'},
        })

        self.assertIn('id="acdVpnRetry"', html)
        self.assertIn('لطفاً فیلترشکن را خاموش کنید', html)
        self.assertIn('aria-modal="true"', html)

    def test_modal_is_absent_for_clean_connection(self):
        html = render_to_string('partials/vpn_block_modal.html', {
            'LANGUAGE_CODE': 'fa',
            'vpn_status': {'blocked': False, 'checked': True, 'reason': ''},
        })

        self.assertNotIn('acd-vpn-gate', html)


@override_settings(ALLOWED_HOSTS=['testserver'])
class VpnModalIntegrationTests(TestCase):
    @patch('apps.core.context_processors.get_vpn_status')
    def test_site_base_includes_gate_for_blocked_connection(self, get_status):
        get_status.return_value = {
            'blocked': True,
            'checked': True,
            'reason': 'vpn',
        }

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="acd-vpn-gate"')
        self.assertContains(response, 'id="acdVpnRetry"')
