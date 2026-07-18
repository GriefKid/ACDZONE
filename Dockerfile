# ACD Zone — single-container image.
#
# Runs everything the site needs from one `docker run`/`docker compose up`:
# migrations, the Telegram support-chat poller (apps/support/management/
# commands/poll_telegram.py), and the Django dev server — see
# docker-entrypoint.sh for the exact order ("migrate first, then start
# the poller in the background, then runserver in the foreground").
#
# This is a development/small-deployment image (runs manage.py runserver,
# not gunicorn/uwsgi) to match how the project already runs locally — see
# README.md if you want to swap in a production WSGI server later.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# gettext: only needed if/when the project switches from the
# apps/core/translations.py dictionary-based translations back to real
# {% trans %}/gettext (see that file's docstring) — harmless to include
# now, cheap, and saves a rebuild later. libjpeg/zlib: Pillow (product/
# post images) needs these to handle JPEG/PNG.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gettext \
        libjpeg62-turbo \
        zlib1g \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
