"""
Minimal Telegram Bot API client — stdlib only (urllib + json), no new
dependency added to requirements.txt for this. Exactly two operations,
because that's all the support-chat <-> Telegram bridge needs:

  - send_message(text): pushes a customer's chat message into the
    Telegram support group. Called from ChatMessage.save() in
    apps/support/models.py. Returns the new Telegram message_id, which
    gets saved back onto that ChatMessage (telegram_message_id) so a
    later reply can be matched back to the right conversation.
  - get_updates(offset): pulls new updates (staff replies) since the
    last-seen one. Called from the poll_telegram management command,
    which should run every minute or so via cron — see README.

Both TELEGRAM_BOT_TOKEN and TELEGRAM_SUPPORT_CHAT_ID come from settings
(ultimately from .env — see .env.example and the README's Telegram
section for how to get real values for both). If either is missing,
these functions are deliberately no-ops (None / []) instead of raising:
Telegram is an optional bridge on top of the on-site chat widget, which
must keep working perfectly whether or not a bot has been configured.
"""
import json
import urllib.error
import urllib.request

from django.conf import settings

API_URL = 'https://api.telegram.org/bot{token}/{method}'


def _call(method, params):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '') or ''
    if not token:
        return None

    url = API_URL.format(token=token, method=method)
    data = json.dumps(params).encode('utf-8')
    request = urllib.request.Request(
        url, data=data, headers={'Content-Type': 'application/json'}, method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        # Network hiccup, bad token, Telegram down, malformed JSON, etc. —
        # never let a Telegram problem break the actual site feature
        # (sending/receiving a support chat message) that triggered this.
        return None

    if not payload.get('ok'):
        return None
    return payload.get('result')


def send_message(text, reply_to_message_id=None):
    """Sends `text` to TELEGRAM_SUPPORT_CHAT_ID. Returns the new message's
    Telegram message_id (int) on success, or None if unconfigured/failed
    — every caller must tolerate None."""
    chat_id = getattr(settings, 'TELEGRAM_SUPPORT_CHAT_ID', '') or ''
    if not chat_id:
        return None

    params = {'chat_id': chat_id, 'text': text}
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id

    result = _call('sendMessage', params)
    return result.get('message_id') if result else None


def get_updates(offset=None):
    """Fetches new updates since `offset` (Telegram's own cursor — see
    TelegramBotState/poll_telegram.py for how it's persisted between
    separate cron runs). Returns [] on any failure or if unconfigured."""
    params = {'timeout': 0, 'allowed_updates': ['message']}
    if offset is not None:
        params['offset'] = offset

    result = _call('getUpdates', params)
    return result or []
