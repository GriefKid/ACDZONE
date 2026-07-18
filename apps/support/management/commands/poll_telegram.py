"""
Picks up staff replies typed in the Telegram support group and turns them
into normal ChatMessage rows (is_staff_reply=True) inside the right
Conversation — the other half of the bridge started in ChatMessage.save()
(apps/support/models.py), which pushes each new *customer* message INTO
that same Telegram group the moment it's sent.

How a reply gets matched back to the right conversation: every message
this bridge posts to Telegram is a real, ordinary Telegram message with
its own message_id, saved onto the originating ChatMessage as
telegram_message_id. When a staff member uses Telegram's native "Reply"
feature on that specific message and types their answer, Telegram's
getUpdates response includes `message.reply_to_message.message_id` — this
command looks that ID up against ChatMessage.telegram_message_id to find
the conversation it belongs to. A plain (non-reply) message typed into
the group is ignored on purpose: there'd be no reliable way to tell which
customer it was meant for.

Two ways to run it, since "right now, locally" and "later, deployed" call
for different things:

  - `python manage.py poll_telegram` (default) loops forever, checking
    every --interval seconds (5 by default). Start it once in its own
    terminal window/tab and leave it running — this is the one to use
    for testing on your own machine right now, no cron/Task Scheduler
    setup needed. Stop it any time with Ctrl+C.
  - `python manage.py poll_telegram --once` checks a single time and
    exits immediately — this is the one to put in a real cron job once
    the site is deployed to a server (see README), or to run as a
    systemd/Windows service instead of this command's own loop.
"""
import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.support.models import ChatMessage, TelegramBotState
from apps.support.telegram_bot import get_updates


class Command(BaseCommand):
    help = 'Polls Telegram for staff replies to forwarded support-chat messages and applies them.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--once', action='store_true',
            help='Check a single time and exit (for cron/systemd). Default: loop forever.',
        )
        parser.add_argument(
            '--interval', type=int, default=5,
            help='Seconds to wait between checks when looping (default: 5).',
        )

    def handle(self, *args, **options):
        if options['once']:
            self._poll_once()
            return

        interval = options['interval']
        self.stdout.write(self.style.SUCCESS(
            f'Watching Telegram for staff replies every {interval}s — press Ctrl+C to stop.'
        ))
        try:
            while True:
                self._poll_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write('\nStopped.')

    def _poll_once(self):
        state = TelegramBotState.load()
        offset = state.last_update_id + 1 if state.last_update_id else None
        updates = get_updates(offset=offset)

        if not updates:
            return

        applied = 0
        highest_update_id = state.last_update_id

        for update in updates:
            highest_update_id = max(highest_update_id, update.get('update_id', 0))

            message = update.get('message') or {}
            reply_to = message.get('reply_to_message')
            text = message.get('text')
            if not reply_to or not text:
                continue  # not a reply to one of our forwarded messages — ignore

            original = (
                ChatMessage.objects
                .filter(telegram_message_id=reply_to.get('message_id'))
                .select_related('conversation')
                .first()
            )
            if not original:
                continue  # reply to some unrelated message already in the group

            staff_sender = self._pick_staff_sender()
            if not staff_sender:
                self.stderr.write('No active staff user found to attribute the reply to — skipping.')
                continue

            ChatMessage.objects.create(
                conversation=original.conversation,
                sender=staff_sender,
                body=text,
                is_staff_reply=True,
            )
            applied += 1

        # Saved even if nothing matched (e.g. someone posted a non-reply
        # message in the group) — otherwise the same non-reply updates
        # would come back on every future check forever.
        state.last_update_id = highest_update_id
        state.save(update_fields=['last_update_id'])

        if applied:
            noun = 'reply' if applied == 1 else 'replies'
            self.stdout.write(self.style.SUCCESS(f'Applied {applied} staff {noun} from Telegram.'))

    @staticmethod
    def _pick_staff_sender():
        # Every reply gets attributed to whichever staff account was
        # created first — good enough for "a small team replies from one
        # shared Telegram group", which is what was actually asked for.
        # If distinct per-admin identity in the chat log ever matters
        # later, this is the one place to extend: map Telegram's
        # message.from.id to a specific site staff account instead of
        # always picking the same one.
        User = get_user_model()
        return User.objects.filter(is_staff=True, is_active=True).order_by('id').first()
