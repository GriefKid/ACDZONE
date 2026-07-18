"""
Daily ACDNews auto-import from Iranian news agency RSS feeds.

Meant to be run once a day by the server's own cron (this project has no
background worker/scheduler of its own — see README for the exact crontab
line to add once the site is deployed). Every run:

  1. Downloads each source's general "latest news" RSS feed (stdlib only —
     urllib + xml.etree — no new dependency added to requirements.txt for
     this).
  2. Takes up to MAX_ITEMS_PER_SOURCE brand-new items per source (skips
     anything whose original link has already been imported before, so
     re-running the same day, or after a missed day, never double-posts).
  3. Classifies each item into ورزشی/اقتصادی/سیاسی/اجتماعی itself, from its
     own title/description text (see classify_category) — the feeds used
     here are each source's *general* feed, not 24 separately-verified
     category feeds across 6 sites.
  4. Creates it as a normal ACDNews Post, with source_name/source_url set
     so the byline and "view original" link (already built into
     templates/blog/acdnews.html and news_detail.html) show up exactly
     like a hand-entered sourced post would.

Usage: python manage.py fetch_news
"""
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.blog.models import (
    CATEGORY_ECONOMY, CATEGORY_POLITICS, CATEGORY_SOCIETY, CATEGORY_SPORTS, CHANNEL_NEWS, Post,
)

# One general "latest news" feed per source, not 4 category feeds x 6
# sources — classification happens in this command instead (see
# classify_category), so only one URL per source needs to stay correct.
# If a source ever moves its feed, this is the only line to fix.
#
# Verified directly (fetched/confirmed via search) at the time this was
# written: ایسنا, ایرنا, تسنیم, باشگاه خبرنگاران جوان. مهر و فارس هم بر
# اساس همون الگوی استاندارد rss خودشونه؛ اگر یک‌وقت هیچ آیتمی از یکی از
# این دو تا اضافه نشد، اول همین آدرس رو دستی توی مرورگر چک کن.
SOURCES = [
    ('خبرگزاری فارس', 'https://www.farsnews.ir/rss'),
    ('ایسنا', 'https://www.isna.ir/rss'),
    ('خبرگزاری مهر', 'https://www.mehrnews.com/rss'),
    ('ایرنا', 'https://www.irna.ir/rss'),
    (
        'خبرگزاری تسنیم',
        'https://www.tasnimnews.com/fa/rss/feed/0/7/0/'
        '%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-'
        '%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B1%D9%88%D8%B2',
    ),
    ('باشگاه خبرنگاران جوان', 'https://www.yjc.ir/fa/rss/allnews'),
]

# "زیاد هم نشه" — کاربر همین رو خواسته: یکی‌دو تا از هر منبع در هر اجرا.
MAX_ITEMS_PER_SOURCE = 2

# Keyword -> category. Checked against the feed's own <category> tag
# first (when a source provides one), then against title+description as
# a fallback. First matching keyword wins.
CATEGORY_KEYWORDS_MAP = {
    CATEGORY_SPORTS: [
        'ورزش', 'فوتبال', 'والیبال', 'بسکتبال', 'کشتی', 'المپیک', 'لیگ برتر',
        'تیم ملی', 'جام جهانی', 'استقلال', 'پرسپولیس', 'کاراته', 'وزنه‌برداری',
        'تنیس', 'شطرنج', 'داور', 'قهرمانی',
    ],
    CATEGORY_ECONOMY: [
        'اقتصاد', 'بورس', 'ارز', 'دلار', 'تورم', 'بانک مرکزی', 'بودجه',
        'مالیات', 'صادرات', 'واردات', 'نفت', 'قیمت', 'بازار', 'تجارت',
        'صنعت', 'کارگر', 'اشتغال', 'خودرو', 'گمرک',
    ],
    CATEGORY_POLITICS: [
        'سیاس', 'مجلس', 'دولت', 'رئیس‌جمهور', 'رئیس جمهور', 'وزیر', 'دیپلماس',
        'سفیر', 'انتخابات', 'شورای نگهبان', 'برجام', 'تحریم', 'سیاست خارجی',
        'نشست', 'مذاکرات', 'وزارت خارجه',
    ],
    CATEGORY_SOCIETY: [
        'اجتماع', 'آموزش و پرورش', 'دانشگاه', 'ترافیک', 'محیط زیست', 'سلامت',
        'بیمارستان', 'زلزله', 'سیل', 'حادثه', 'پلیس', 'دادگاه', 'قضایی',
        'خانواده', 'مسکن', 'بیمه',
    ],
}


def classify_category(title, description, rss_category):
    text = ' '.join([rss_category or '', title or '', description or ''])
    for category, keywords in CATEGORY_KEYWORDS_MAP.items():
        for kw in keywords:
            if kw in text:
                return category
    # Safe default rather than leaving it blank — a blank category means
    # the post is invisible to ACDNews's four filter pills until an admin
    # manually classifies it (see templates/blog/acdnews.html).
    return CATEGORY_SOCIETY


def strip_html(text):
    """RSS <description> is frequently a raw HTML snippet — Post.body is
    rendered through the plain |linebreaks filter (see
    templates/blog/news_detail.html), so tags need stripping here rather
    than leaking onto the page as literal text."""
    if not text:
        return ''
    return re.sub(r'<[^>]+>', '', text).strip()


def parse_pub_date(raw):
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return None
    if dt is not None and timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    return dt


class Command(BaseCommand):
    help = (
        'Pulls 1-2 fresh items from each configured Iranian news agency '
        'RSS feed and adds them to ACDNews, tagged with their source and '
        'auto-classified into ورزشی/اقتصادی/سیاسی/اجتماعی. Run once a day '
        'from cron; safe to re-run manually any time (already-imported '
        'items are skipped by their original link).'
    )

    def handle(self, *args, **options):
        total_created = 0

        for source_name, feed_url in SOURCES:
            try:
                items = self._fetch_feed_items(feed_url)
            except (urllib.error.URLError, ET.ParseError, TimeoutError, ValueError) as exc:
                self.stderr.write(f'{source_name}: could not fetch/parse feed ({exc}) — skipping.')
                continue

            created_for_source = 0
            for item in items:
                if created_for_source >= MAX_ITEMS_PER_SOURCE:
                    break

                link = (item.get('link') or '').strip()
                title = (item.get('title') or '').strip()
                if not link or not title:
                    continue
                if Post.objects.filter(source_url=link).exists():
                    continue  # already imported on an earlier run

                description = strip_html(item.get('description'))
                category = classify_category(title, description, item.get('category'))

                Post.objects.create(
                    channel=CHANNEL_NEWS,
                    category=category,
                    title=title[:220],
                    summary=description[:500],
                    body=description or title,
                    source_name=source_name,
                    source_url=link,
                    image_url=item.get('image_url') or '',
                    published_at=item.get('pub_date') or timezone.now(),
                )
                created_for_source += 1
                total_created += 1

            self.stdout.write(f'{source_name}: added {created_for_source} new post(s).')
            time.sleep(1)  # small courtesy delay between sources

        self.stdout.write(self.style.SUCCESS(
            f'Done — {total_created} new ACDNews post(s) added in total.'
        ))

    def _fetch_feed_items(self, feed_url):
        request = urllib.request.Request(feed_url, headers={'User-Agent': 'ACDZoneNewsBot/1.0'})
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read()

        root = ET.fromstring(raw)
        items = []
        for item_el in root.findall('.//item'):
            def text_of(tag, _el=item_el):
                found = _el.find(tag)
                return found.text if found is not None and found.text else ''

            enclosure = item_el.find('enclosure')
            image_url = enclosure.get('url', '') if enclosure is not None else ''

            items.append({
                'title': text_of('title'),
                'link': text_of('link'),
                'description': text_of('description'),
                'category': text_of('category'),
                'pub_date': parse_pub_date(text_of('pubDate')),
                'image_url': image_url,
            })
        return items
