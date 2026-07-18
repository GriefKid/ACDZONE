#!/bin/sh
# Container start order (this is what the user asked for): migrate first,
# then start the Telegram support-chat poller in the background, then run
# the dev server in the foreground so `docker logs` follows it and the
# container stays up as long as the server does.
set -e

echo "[entrypoint] Applying database migrations..."
python manage.py migrate --noinput

echo "[entrypoint] Starting Telegram poller (apps/support/management/commands/poll_telegram.py) in the background..."
# Only actually polls if TELEGRAM_BOT_TOKEN is set (see
# apps/support/management/commands/poll_telegram.py /
# apps/support/telegram_bot.py) — safe to always start, it just no-ops
# quietly otherwise instead of crashing the container.
python manage.py poll_telegram &

echo "[entrypoint] Starting Django dev server on 0.0.0.0:8000..."
exec python manage.py runserver 0.0.0.0:8000
